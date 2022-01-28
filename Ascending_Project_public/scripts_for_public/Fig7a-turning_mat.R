library(tidyr)
library(dplyr)
library(reshape2)
source("utils_Florian.R")

behaviours <- c("rest", "forward_walking", "antennal_grooming", "eye_grooming", "foreleg_grooming", "hindleg_grooming", "abdominal_grooming", "PER_event")
n_repetitions <- 5
base_folder <- paste(root_dir, "Ascending_Project_public/output/Fig7a_7c-turning/", sep="")
dir.create(base_folder)
plot_folder <- paste(base_folder, "plots/", sep="")
dir.create(plot_folder)

intercept <- TRUE
standardize <- FALSE
standardize.response <- FALSE
non_negative_regressors <- c()
possible_crf_parameters <- read.csv(paste(root_dir, "Ascending_Project_public/output/Fig2_S4-GLM_jangles_legs_beh_DFF/crf_parameters.csv",sep=""))


examples <- list(list("genotype"="SS34574", "roi_0"=0, "roi_1"=1),
                 list("genotype"="SS51046", "roi_0"=0, "roi_1"=1),
                 list("genotype"="SS29893", "roi_0"=0, "roi_1"=2),
                 list("genotype"="SS29893", "roi_0"=0, "roi_1"=3),
                 list("genotype"="SS29893", "roi_0"=2, "roi_1"=3),

                 list("genotype"="SS41806", "roi_0"=0, "roi_1"=1),
                 list("genotype"="SS44270", "roi_0"=0, "roi_1"=1),
                 list("genotype"="SS31219", "roi_0"=0, "roi_1"=1),
                 list("genotype"="SS51017", "roi_0"=0, "roi_1"=1),
                 list("genotype"="SS51021", "roi_0"=0, "roi_1"=1),
                 list("genotype"="SS29621", "roi_0"=0, "roi_1"=1),
                 
                 list("genotype"="SS28596", "roi_0"=0, "roi_1"=1),
                 list("genotype"="SS28596", "roi_0"=0, "roi_1"=2),
                 list("genotype"="SS28596", "roi_0"=0, "roi_1"=3),
                 list("genotype"="SS28596", "roi_0"=0, "roi_1"=4),
                 list("genotype"="SS28596", "roi_0"=0, "roi_1"=5),
                 list("genotype"="SS28596", "roi_0"=1, "roi_1"=2),
                 list("genotype"="SS28596", "roi_0"=1, "roi_1"=3),
                 list("genotype"="SS28596", "roi_0"=1, "roi_1"=4),
                 list("genotype"="SS28596", "roi_0"=1, "roi_1"=5),
                 list("genotype"="SS28596", "roi_0"=2, "roi_1"=3),
                 list("genotype"="SS28596", "roi_0"=2, "roi_1"=4),
                 list("genotype"="SS28596", "roi_0"=2, "roi_1"=5),
                 list("genotype"="SS28596", "roi_0"=3, "roi_1"=4),
                 list("genotype"="SS28596", "roi_0"=3, "roi_1"=5),
                 list("genotype"="SS28596", "roi_0"=4, "roi_1"=5),
                 
                 list("genotype"="SS40619", "roi_0"=0, "roi_1"=1),
                 list("genotype"="R36G04", "roi_0"=0, "roi_1"=1),
                 list("genotype"="MAN", "roi_0"=0, "roi_1"=1),                

                 list("genotype"="SS49172", "roi_0"=0, "roi_1"=1),
                 list("genotype"="SS49172", "roi_0"=0, "roi_1"=2),
                 list("genotype"="SS49172", "roi_0"=1, "roi_1"=2),

                 list("genotype"="R70H06", "roi_0"=0, "roi_1"=1),
                 list("genotype"="SS42740", "roi_0"=0, "roi_1"=1),
                 list("genotype"="SS42749", "roi_0"=0, "roi_1"=1),

                 list("genotype"="R85A11", "roi_0"=2, "roi_1"=4),
                 list("genotype"="R85A11", "roi_0"=2, "roi_1"=5),
                 list("genotype"="R85A11", "roi_0"=4, "roi_1"=5),
                 
                 list("genotype"="SS29579", "roi_0"=0, "roi_1"=1),
                 list("genotype"="SS29579", "roi_0"=0, "roi_1"=2),
                 list("genotype"="SS29579", "roi_0"=0, "roi_1"=3),
                 list("genotype"="SS29579", "roi_0"=1, "roi_1"=2),
                 list("genotype"="SS29579", "roi_0"=1, "roi_1"=3),
                 list("genotype"="SS29579", "roi_0"=2, "roi_1"=3),

                 list("genotype"="SS36118", "roi_0"=3, "roi_1"=4),
                 list("genotype"="SS38592", "roi_0"=3, "roi_1"=4),
                 list("genotype"="SS31480", "roi_0"=0, "roi_1"=2),
                 list("genotype"="SS46233", "roi_0"=0, "roi_1"=1),
                 list("genotype"="SS41815", "roi_0"=0, "roi_1"=1),
                 
                 list("genotype"="SS45363", "roi_0"=0, "roi_1"=1),
                 list("genotype"="SS45363", "roi_0"=0, "roi_1"=2),
                 list("genotype"="SS45363", "roi_0"=0, "roi_1"=3),
                 list("genotype"="SS45363", "roi_0"=1, "roi_1"=2),
                 list("genotype"="SS45363", "roi_0"=1, "roi_1"=3),
                 list("genotype"="SS45363", "roi_0"=2, "roi_1"=3)
                )



all_results_turning <- data.frame()
all_results_speed <- data.frame()
for (example in examples){
    genotype <- example[["genotype"]]
    roi_0 <- example[["roi_0"]]
    roi_1 <- example[["roi_1"]]
    print("###############################################")
    print(paste(genotype, roi_0, roi_1))
    print("###############################################")
    folder <- paste(base_folder, "plots", paste(genotype, roi_0, roi_1, sep="_"), sep="/")
    # dir.create(folder)
    df <- read.csv.with.nan(paste(root_dir,"Ascending_Project_public/output/Fig2_S4-GLM_jangles_legs_beh_DFF/glm_input_files/", genotype, ".csv", sep=""))
    if (length(unique(df$Fly)) != 1){
        stop("more than one fly")
    }
    df <- df[df$dFF_processing == "raw" & df$Regressor_processing == "raw", ]
    df <- df[, names(df) != "X"]
    df$Proboscis.extension.marker <- NA
    df[df$PER_event > 0, "Proboscis.extension.marker"] <- "PE"

    # Fix units of optical flow
    df[, "Yaw"] <- df[, "Yaw"] * 360
    df[, "Roll"] <- df[, "Roll"] * pi * 10

    trials <- unlist(unique(df["Trial"]))
    rois <- unlist(unique(df$ROI))
    for (roi in rois){
        df[df$ROI == roi,] <- apply_filter_to_trials(df[df$ROI == roi,], "dFF", moving_average)
        df[df$ROI == roi,] <- apply_filter_to_trials(df[df$ROI == roi,], "Yaw", moving_average)
        df[df$ROI == roi,] <- apply_filter_to_trials(df[df$ROI == roi,], "Roll", moving_average)
        df[df$ROI == roi,] <- apply_filter_to_trials(df[df$ROI == roi,], "Pitch", moving_average)
    }
    
    df_roi_0 <- df[df[,"ROI"] == roi_0, colnames(df) != "ROI"]
    df_roi_1 <- df[df[,"ROI"] == roi_1, colnames(df) != "ROI"]
    names(df_roi_0)[names(df_roi_0) == "dFF"] <- paste("dFF", "0", sep="_")
    names(df_roi_1)[names(df_roi_1) == "dFF"] <- paste("dFF", "1", sep="_")
    diff_df <- merge(df_roi_0, df_roi_1[,c("Date", "Genotype", "Fly", "Trial", "Frame_times", "dFF_1")])
    
    diff_df[,"dFF"] <- diff_df[,"dFF_1"] - diff_df[,"dFF_0"]
    
    # Regression with yaw and diff dFF
    for (regressor in c("Yaw", "Roll")){
        
        parameters = find_best_crf_parameters(diff_df, regressor, possible_crf_parameters, non_negative_regressors, standardize, standardize.response)
        a <- parameters["a"]
        b <- parameters["b"]

        diff_df <- convolve_with_crf(diff_df, regressor, a, b)
        regressor_conv <- paste(regressor, "conv", sep=".")
       
        diff_df$blanc <- 0
        diff_df$fold <- get_folds(diff_df, "blanc")
        for (fold in 1:10){
            test_data <- data.frame(diff_df[diff_df$fold == fold,])
            train_data <- data.frame(diff_df[diff_df$fold != fold,])

            complete_results <- model_function(train_data, test_data, regressor_conv, non_negative_regressors, 0, standardize=standardize, standardize.response=standardize.response, intercept=intercept)
            p_value <- complete_results[["F p-value"]]
            y_test <- as.vector(test_data[, "dFF"])
            y_hat <- complete_results[["prediction"]]
            r_squared <- complete_results[["r.squared"]]

            all_results_turning <- rbind(all_results_turning, data.frame("Genotype"=genotype,
                                                         "ROI.0"=roi_0,
                                                         "ROI.1"=roi_1,
                                                         "Genotype_ROI"=paste(genotype, roi_0, roi_1),
                                                         "Explained_variance"=r_squared,
                                                         "p.value"=p_value,
                                                         "Regressor"=regressor,
                                                         "Fold"=fold
                                                        )
                                )
        }
        
        raw_df <- data.frame(diff_df)
        raw_df[,"Lines"] <- "%dF/F"

        for (trial in unique(diff_df$Trial)){
            trial_df <- diff_df[diff_df$Trial == trial,]
            
            complete_results <- model_function(trial_df, trial_df, regressor_conv, non_negative_regressors, 0, standardize=standardize, standardize.response=standardize.response, intercept=intercept)
            p_value <- complete_results[["F p-value"]]
            y_hat <- complete_results[["prediction"]]
            r_squared <- complete_results[["r.squared"]]

            prediction_df <- data.frame(trial_df)
            prediction_df[,"Lines"] <- "Regressor only"
            prediction_df[,"dFF"] <- y_hat
            annotation_r_squared <- paste("R\u00B2=", sprintf("%4.2f", r_squared), sep="")
            annotation_p_value <- paste('italic(p)*"-value" ==', sprintf("%4.2e", p_value))
            plot_df <- rbind(raw_df, prediction_df)
            plot_df <- rename_behaviours(plot_df)
            output_file <- paste(folder, "/diff_regression_", regressor, "_trial_", trial, ".pdf", sep="")
            #plot_predictions(plot_df[plot_df$Trial == trial,], output_file, annotation_r_squared)
        }
        output_file <- paste(folder, "/scatter_", regressor, ".pdf", sep="")
        if (regressor == "Yaw"){
            x_label <- expression(v["rotation"]*"(deg/s)")
        } else if (regressor == "Roll"){
            x_label <- expression(v["side"]*"(mm/s)")
        }
        model <- lm(as.formula(paste("dFF ~", regressor)), diff_df)
        r.squared <- summary(model)$r.squared 
        # plot_scatter(diff_df, regressor_conv, output_file, x_label=x_label,
        #              annotation_1=paste("R\u00B2=", sprintf("%4.2f", r.squared), sep=""),
        #              size=c(3, 4)
        #             )
    }
}

all_results_turning[,"p.value"] <- p.adjust(all_results_turning[,"p.value"], "bonferroni")
write.csv(all_results_turning, paste(base_folder, "/all_results_turning.csv", sep=""))
all_results_turning <- read.csv(paste(base_folder, "/all_results_turning.csv", sep=""))

all_results_turning <- all_results_turning %>% group_by(Genotype, ROI.0, ROI.1, Genotype_ROI, Regressor) %>% dplyr::summarize(Explained_variance = mean(Explained_variance), p.value = max(p.value))
all_results_turning[, "Significance.stars"] <- ""
all_results_turning <- all_results_turning %>% mutate(Significance.stars=replace(Significance.stars, p.value < 0.05, "  *"))
all_results_turning <- all_results_turning %>% mutate(Significance.stars=replace(Significance.stars, p.value < 0.01, " **"))
all_results_turning <- all_results_turning %>% mutate(Significance.stars=replace(Significance.stars, p.value < 0.001, "***"))

genotype.order <- read.csv(paste(root_dir, "Ascending_Project_public/scripts_for_public/utils/genotype_order.csv")[["x"]]
all_results_turning[,"Genotype.ranks"] <- match(all_results_turning$Genotype, genotype.order)
row.order <- all_results_turning[order(all_results_turning$Genotype.ranks, all_results_turning$ROI.0, all_results_turning$ROI.1), "Genotype_ROI"]
row.order <- pull(row.order, "Genotype_ROI")

all_results_turning <- all_results_turning %>% unite("ROI", c("ROI.0", "ROI.1"), remove = FALSE, sep="\n-\n")

justifications=c(neuron_num_vjust=9.5, driver_line_vjust=13, gal4_hjust=4, gal4_line_y=0.13)
output_file <- paste(plot_folder, "turning_r_squared_mean_matrix.pdf", sep="")
plot_matrix(all_results_turning, "Explained_variance", row.order, "Explained variance, cross-validation mean (%)", output_file, text_col="Significance.stars", justifications=justifications, as_perc=TRUE)


