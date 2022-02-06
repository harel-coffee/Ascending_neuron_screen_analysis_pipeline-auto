library(ggplot2)
library(tidyverse)
library(ggpmisc)
# library(ggrepel)
# library(broom)

source("utils_Florian.R")

# dir.create(paste(root_dir, "output/Fig10a_10c-PE_analysis/", sep=""))
dir.create(paste(root_dir, "Ascending_neuron_screen_analysis_pipeline/output/Fig10a_10c-PE_analysis/plots/", sep=""))

possible_crf_parameters <- read.csv(paste(root_dir, "Ascending_neuron_screen_analysis_pipeline/output/Fig2_S4-GLM_jangles_legs_beh_DFF/crf_parameters.csv", sep=""))
intercept <- TRUE
standardize <- FALSE
standardize.response <- FALSE

df <- read.csv.with.nan(paste(root_dir, "Ascending_neuron_screen_analysis_pipeline/output/Fig2_S4-GLM_jangles_legs_beh_DFF/glm_input_files/SS31232.csv", sep=""))

# window_sizes <- seq(1, 2400, 8)
window_sizes <- seq(1, 1200, 10)
# window_sizes <- seq(1, 1200, 240)

span_for_max=as.integer(1200/(10*1.5))

for (window_size in window_sizes){
    print(window_size)
    kernel <- rep(1, window_size)
    for (t in unique(df$Trial)){
        for (roi in unique(df$ROI)){
            x <- df[(df$Trial == t) & (df$ROI == roi), "PER_event"]
            convolved <- convolve(x, kernel, type="open")
            pre_col <- paste("PER_pre", window_size, sep="_")
            if (window_size == 1){
                df[df$Trial == t, pre_col] <- df[df$Trial == t, "PER_event"]
            } else {
                start <- 1
                stop <- length(x)
                df[df$Trial == t, pre_col] <- convolved[start:stop]
            }
        }
    }
    for (pos in c("pre")){
        col <- paste("PER", pos, window_size, sep="_")
        masked_col <- paste("PER_masked", pos, window_size, sep="_")
        df[, masked_col] <- df[,col]
        df[!df$PER_event, masked_col] <- 0
    }
}

df$blanc <- 0
for (roi in unique(df$ROI)){
    df[df$ROI == roi, "fold"] <- get_folds(df[df$ROI == roi,], "blanc")
    df[df$ROI == roi,] <- apply_filter_to_trials(df[df$ROI == roi,], "dFF", moving_average)
}

results <- data.frame()
for (pos in c("masked_pre")){
    for(window_size in window_sizes){
        for (roi in unique(df$ROI)){
            regressor <- paste("PER", pos, window_size, sep="_")
            df_roi <- df[df$ROI == roi,]
            parameters = find_best_crf_parameters(df_roi, regressor, possible_crf_parameters, regressor, standardize, standardize.response)
            a <- parameters["a"]
            b <- parameters["b"]
            df_roi <- convolve_with_crf(df_roi, regressor, a, b)
            regressor <- paste(regressor, "conv", sep=".")
            formula <- as.formula(paste("dFF ~", regressor))
            for (fold in unique(df$fold)){
                train_data <- df_roi[(df_roi$fold != fold),]
                test_data <- df_roi[(df_roi$fold == fold),]
                lambda <- estimate_lambda(train_data, regressor, "blanc", regressor, standardize, standardize.response, intercept=intercept)
                r.squared <- model_function(train_data, test_data, regressor, regressor, lambda=lambda, standardize=standardize, standardize.response=standardize.response, intercept=intercept)[["r.squared"]]
                current_observation <- data.frame("Position"=pos,
                                                  "Window.size"=window_size,
                                                  "r.squared"=r.squared,
                                                  "Fold"=fold,
                                                  "ROI"=roi)
                results <- rbind(results, current_observation)
            }
        }
    }
}
write.csv(results, paste(root_dir, "Ascending_neuron_screen_analysis_pipeline/output/Fig10a_10c-PE_analysis/PER_results.csv", sep=""))
results <- read.csv(paste(root_dir, "Ascending_neuron_screen_analysis_pipeline/output/Fig10a_10c-PE_analysis/PER_results.csv", sep=""))
results <- results %>% group_by_at(c("ROI", "Position", "Window.size")) %>% summarize_at(vars(-group_cols(), -Fold), list("mean"=mean, "sem"=sem))
results[, "r.squared_mean"] <- results[, "r.squared_mean"] * 100
dt <- c()
for (trial in unique(df$Trial)){
    dt <- c(dt, diff(df[(df$Trial == trial) & (df$ROI == 0), "Frame_times"]))
}
dt <- mean(dt)
results[, "Windowtime"] <- results[, "Window.size"] * dt 

# results_2 <- results %>%
#   group_by(ROI) %>%
#   mutate(color = (max(r.squared_mean) == r.squared_mean))


# results %>%
#   group_by(ROI) %>%
#   summarise(min = min(r.squared_mean),
#             max = max(r.squared_mean)) -> results_2

# left_join(results, results_2) %>%
#   mutate(color = (min(r.squared_mean) == r.squared_mean | max(r.squared_mean) == r.squared_mean)) %>%
#   filter(color == TRUE) -> results_3



size_factor <- 2.134
p <- ggplot(data=results, aes(x=Windowtime, y=r.squared_mean, color=factor(ROI))) +
        geom_line(size = 0.5 / size_factor) +
        # geom_point(data=results_2, aes(x = Windowtime, y = r.squared_mean), color = "red") + 
        # geom_point(aes(color = color)) + 
        stat_peaks(color="red", strict=TRUE, span = span_for_max)+
        #scale_color_manual(values = c(NA, "red"))+
        theme(panel.grid.major = element_blank(),
              panel.grid.minor = element_blank(),
              panel.background = element_rect(fill="transparent"),
              axis.line = element_line(colour = "black", size=0.5 / size_factor, lineend = "square"),
              text = element_text(family="Arial", colour = "black", size=6),
              axis.text = element_text(family="Arial", colour = "black", size=4),
              axis.ticks = element_line(colour = "black", size=0.5 / size_factor),
              axis.ticks.length = unit(1.522, "pt"),
              axis.text.y = element_text(family="Arial", colour = "black", size=4),
              legend.key.size = unit(0.6, "line"),
              legend.title=element_text(family="Arial", colour="black", size=6),
              legend.text=element_text(family="Arial", colour="black", size=4),
              ) +
        labs(x="Window size (s)", y="R\u00B2 (%)")

ggsave(paste(root_dir, "Ascending_neuron_screen_analysis_pipeline/output/Fig10a_10c-PE_analysis/plots/PER.pdf", sep=""), height=6, width=15, scale=0.25, device=cairo_pdf)

for (roi in unique(df$ROI)){
    for (position in c("masked_pre")){
        roi_results <- results[(results$ROI == roi) & (results$Position == position),]
        window_size <- unlist(roi_results[which.max(roi_results$r.squared_mean), "Window.size"])
        position <- unlist(roi_results[which.max(roi_results$r.squared_mean), "Position"])
        regressor <- paste("PER", position, window_size, sep="_")
        roi_df <- df[df$ROI == roi,]
        roi_df <- apply_filter_to_trials(roi_df, "dFF", moving_average)
        regressors <- c(regressor, paste("PER", position, "1", sep="_"))
        for (regressor in regressors){
            parameters = find_best_crf_parameters(roi_df, regressor, possible_crf_parameters, regressor, standardize, standardize.response)
            a <- parameters["a"]
            b <- parameters["b"]
            roi_df <- convolve_with_crf(roi_df, regressor, a, b)
            regressor_conv = paste(regressor, "conv", sep=".")
            for (trial in unique(roi_df$Trial)){
                trial_df <- roi_df[roi_df$Trial == trial,]
                raw_df <- data.frame(trial_df)
                raw_df["Lines"] <- "%dF/F"
                raw_df["lower_bound"] <- raw_df["dFF"]
                raw_df["upper_bound"] <- raw_df["dFF"]
        
                regressor_only_model_df <- data.frame(trial_df)
                regressor_only_model_df["Lines"] <- "Prediction"
                complete_results <- model_function(trial_df, trial_df, regressor_conv, regressor_conv, 0, standardize=standardize, standardize.response=standardize.response, intercept=intercept)
                regressor_only_model_df["dFF"] <- complete_results[["prediction"]]
                r_squared <- complete_results[["r.squared"]]
                regressor_only_model_df["lower_bound"] <- regressor_only_model_df["dFF"]
                regressor_only_model_df["upper_bound"] <- regressor_only_model_df["dFF"]
                annotation <- paste("R\u00B2=", sprintf("%4.2f", r_squared), sep="")
                
                regressor_only_model_no_conv_df <- data.frame(trial_df)
                regressor_only_model_no_conv_df["Lines"] <- "Regressor"
                complete_results <- model_function(trial_df, trial_df, regressor, regressor, 0, standardize=standardize, standardize.response=standardize.response, intercept=intercept)
                regressor_only_model_no_conv_df["dFF"] <- complete_results[["prediction"]]
                r_squared <- complete_results[["r.squared"]]
                regressor_only_model_no_conv_df["lower_bound"] <- regressor_only_model_no_conv_df["dFF"]
                regressor_only_model_no_conv_df["upper_bound"] <- regressor_only_model_no_conv_df["dFF"]
        
                plot_df <- rbind(raw_df, regressor_only_model_no_conv_df, regressor_only_model_df)
                output_file <- paste(paste(root_dir, "Ascending_neuron_screen_analysis_pipeline/output/Fig10a_10c-PE_analysis/plots/Trial", sep=""), trial, "ROI", roi, regressor, ".pdf", sep="_")
                print(output_file)
                plot_df <- rename_behaviours(plot_df)
                plot_predictions(plot_df, output_file, annotation)
            }
        }
    }
}
