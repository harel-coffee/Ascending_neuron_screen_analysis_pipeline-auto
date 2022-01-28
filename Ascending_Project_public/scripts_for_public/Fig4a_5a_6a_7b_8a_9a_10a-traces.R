library(tidyr)
source("utils_Florian.R")

behaviours <- c("rest", "forward_walking", "backward_walking", "antennal_grooming", "eye_grooming", "foreleg_grooming", "hindleg_grooming", "abdominal_grooming", "PER_event", "CO2")
intercept <- TRUE
standardize <- FALSE
standardize.response <- FALSE
non_negative_regressors <- paste(behaviours, "conv", sep=".")
possible_crf_parameters <- read.csv(paste(root_dir, "Ascending_Project_public/output/Fig2_S4-GLM_jangles_legs_beh_DFF/crf_parameters.csv", sep=""))

dir.create(paste(root_dir, "Ascending_Project_public/output/Fig2_S4-GLM_jangles_legs_beh_DFF/glm_input_files/",sep=""))



examples = list(list("Genotype"="SS27485", "Regressor"="rest"),
                list("Genotype"="SS29579", "Regressor"=c("forward_walking", "backward_walking")),
                list("Genotype"="SS42740", "Regressor"=c("forward_walking", "backward_walking", "eye_grooming", "antennal_grooming", "foreleg_grooming")),
                list("Genotype"="SS25469", "Regressor"="eye_grooming"),
                list("Genotype"="SS31232", "Regressor"="PER_event"),
                list("Genotype"="SS51046", "Regressor"=c("forward_walking", "backward_walking")),
                list("Genotype"="SS36112", "Regressor"=c("CO2")) #list("Genotype"="SS51046", "Regressor"=c("CO2", "backward_walking")), #list("Genotype"="SS51046", "Regressor"=c("backward_walking"))

               )




for (example in examples){
    genotype <- example["Genotype"]
    print(genotype)
    dir.create(paste(root_dir,"Ascending_Project_public/output/Fig4a5a6a7b8a9a10a-representativeDFF_traces/plots/", genotype, sep=""))
    regressor <- unlist(example["Regressor"])
    df <- read.csv.with.nan(paste(root_dir, "Ascending_Project_public/output/Fig2_S4-GLM_jangles_legs_beh_DFF/glm_input_files/", genotype, ".csv", sep=""))
    for (behaviour in behaviours){
        df[df[[behaviour]] == "", behaviour] = "False"
        df[is.na(df[[behaviour]]), behaviour] = "False"
        df[[behaviour]] <- as.numeric(as.logical(df[[behaviour]]))
    }
    df <- df[df$dFF_processing == "raw" & df$Regressor_processing == "raw", ]
    df <- df[, names(df) != "X"]
    
    if (length(unique(df["Fly"])) != 1){
        print(unique(df["Fly"]))
        stop("more than one fly")
    }
    if (length(unique(df["Date"])) != 1){
        print(unique(df["Date"]))
        stop("more than one date")
    }
    rois <- unlist(unique(df$ROI))
    for (roi in rois){
        roi_df <- df[df$ROI == roi,]
        longer_moving_average <- function(x){
            x <- moving_average(x, 35)
        }
        roi_df <- apply_filter_to_trials(roi_df, "dFF", longer_moving_average)
        parameters = find_best_crf_parameters(roi_df, regressor, possible_crf_parameters, non_negative_regressors, standardize, standardize.response)
        a <- parameters["a"]
        b <- parameters["b"]
        roi_df <- convolve_with_crf(roi_df, regressor, a, b)
        regressor_conv = paste(regressor, "conv", sep=".")

        trials <- unlist(unique(df["Trial"]))
        for (trial in trials){
            trial_df <- roi_df[roi_df$Trial == trial,]
            raw_df <- data.frame(trial_df)
            raw_df["Lines"] <- "%dF/F"
            raw_df["lower_bound"] <- raw_df["dFF"]
            raw_df["upper_bound"] <- raw_df["dFF"]
            
            regressor_only_model_df <- data.frame(trial_df)
            regressor_only_model_df["Lines"] <- "Prediction"
            if (var(trial_df[regressor_conv]) == 0){
                next
            }
            complete_results <- model_function(trial_df, trial_df, regressor_conv, non_negative_regressors, 0, standardize=standardize, standardize.response=standardize.response, intercept=intercept)
            regressor_only_model_df["dFF"] <- complete_results[["prediction"]]
            r_squared <- complete_results[["r.squared"]]
            regressor_only_model_df["lower_bound"] <- regressor_only_model_df["dFF"]
            regressor_only_model_df["upper_bound"] <- regressor_only_model_df["dFF"]
            annotation <- paste("R\u00B2=", sprintf("%4.2f", r_squared), sep="")
            
            plot_df <- rbind(raw_df, regressor_only_model_df)
            output_file <- paste(root_dir,"Ascending_Project_public/output/Fig4a5a6a7b8a9a10a-representativeDFF_traces/", genotype, "/", genotype, "_Trial", trial, "_ROI", roi, ".pdf", sep="")
            plot_df <- rename_behaviours(plot_df)
            plot_predictions(plot_df, output_file, annotation)
        }
    }
}
