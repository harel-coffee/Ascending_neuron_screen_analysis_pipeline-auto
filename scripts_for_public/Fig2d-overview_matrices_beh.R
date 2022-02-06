source("utils_Florian.R")

# behaviours <- c("rest", "walking", "antennal_grooming", "eye_grooming", "foreleg_grooming", "hindleg_grooming", "abdominal_grooming", "PER_event", "pushing", "CO2")    
behaviours <- c("rest", "forward_walking", "backward_walking", "antennal_grooming", "eye_grooming", "foreleg_grooming", "hindleg_grooming", "abdominal_grooming", "PER_event", "pushing", "CO2")
angles = c(
           "Angle.LF_leg.yaw",    "Angle.LF_leg.pitch",  "Angle.LF_leg.roll",
           "Angle.LF_leg.th_fe",   "Angle.LF_leg.th_ti",   "Angle.LF_leg.roll_tr",
           "Angle.LF_leg.th_ta",   "Angle.LM_leg.yaw",     "Angle.LM_leg.pitch",
           "Angle.LM_leg.roll",    "Angle.LM_leg.th_fe",   "Angle.LM_leg.th_ti",
           "Angle.LM_leg.roll_tr", "Angle.LM_leg.th_ta",   "Angle.LH_leg.yaw",
           "Angle.LH_leg.pitch",   "Angle.LH_leg.roll",    "Angle.LH_leg.th_fe",
           "Angle.LH_leg.th_ti",   "Angle.LH_leg.roll_tr", "Angle.LH_leg.th_ta",
           "Angle.RF_leg.yaw",     "Angle.RF_leg.pitch",   "Angle.RF_leg.roll",
           "Angle.RF_leg.th_fe",   "Angle.RF_leg.th_ti",   "Angle.RF_leg.roll_tr",
           "Angle.RF_leg.th_ta",   "Angle.RM_leg.yaw",     "Angle.RM_leg.pitch",
           "Angle.RM_leg.roll",    "Angle.RM_leg.th_fe",   "Angle.RM_leg.th_ti",
           "Angle.RM_leg.roll_tr", "Angle.RM_leg.th_ta",   "Angle.RH_leg.yaw",
           "Angle.RH_leg.pitch",   "Angle.RH_leg.roll",    "Angle.RH_leg.th_fe",
           "Angle.RH_leg.th_ti",   "Angle.RH_leg.roll_tr", "Angle.RH_leg.th_ta"
          )
possible_crf_parameters <- read.csv(paste(root_dir,"Ascending_neuron_screen_analysis_pipeline/output/Fig2_S4-GLM_jangles_legs_beh_DFF/crf_parameters.csv", sep=""))
# print(paste(root_dir,"Ascending_neuron_screen_analysis_pipeline/output/Fig2_S4-GLM_jangles_legs_beh_DFF/crf_parameters.csv", sep=""))


##---------------------------------------------------##
# Choose the regressors to analyze
##---------------------------------------------------##


folder <- paste(root_dir,"Ascending_neuron_screen_analysis_pipeline/output/Fig2_S4-GLM_jangles_legs_beh_DFF/overview_beh/", sep="")      
dir.create(folder)
intercept <- TRUE
standardize <- FALSE
standardize.response <- FALSE
all_regressors <- behaviours
non_negative_regressors <- paste(all_regressors, "conv", sep=".")
regressor_groups <- paste(all_regressors, "conv", sep=".") 
names(regressor_groups) <- all_regressors

##---------------------------------------------------##


# folder <- paste(root_dir,"Ascending_neuron_screen_analysis_pipeline/output/Fig2_S4-GLM_jangles_legs_beh_DFF/overview_angles/", sep="")                     
# dir.create(folder)
# intercept <- TRUE
# standardize <- TRUE
# standardize.response <- FALSE
# all_regressors <- angles
# non_negative_regressors <- c()
# regressor_groups <- paste(all_regressors, "conv", sep=".")
# names(regressor_groups) <- all_regressors

##---------------------------------------------------##


# folder <- paste(root_dir,"Ascending_neuron_screen_analysis_pipeline/output/Fig2_S4-GLM_jangles_legs_beh_DFF/overview_legs/", sep="")           

# dir.create(folder)
# intercept <- TRUE
# standardize <- TRUE
# standardize.response <- FALSE
# all_regressors <- angles
# non_negative_regressors <- c()
# regressor_groups <- list()
# for (name in c("LF", "LM", "LH", "RF", "RM", "RH")){
#    if (name == "LF"){group_name <- "Left front leg"
#    } else if (name == "LM"){group_name <- "Left middle leg"
#    } else if (name == "LH"){group_name <- "Left hind leg"
#    } else if (name == "RF"){group_name <- "Right front leg"
#    } else if (name == "RM"){group_name <- "Right middle leg"
#    } else if (name == "RH"){group_name <- "Right hind leg"}
#    regressor_groups[[group_name]] <- paste(angles[grepl(name, angles)], "conv", sep=".")
# }

##---------------------------------------------------##


# folder <- paste(root_dir,"Ascending_neuron_screen_analysis_pipeline/output/Fig2_S4-GLM_jangles_legs_beh_DFF/overview_leg_pairs/", sep="")           
# dir.create(folder)
# intercept <- TRUE
# standardize <- TRUE
# standardize.response <- FALSE
# all_regressors <- angles
# non_negative_regressors <- c()
# regressor_groups <- list()


# group_name <- "Left front leg - Right front leg"
# for (name in c("LF", "RF")){
#    regressor_groups[[group_name]] <- append(regressor_groups[[group_name]], paste(angles[grepl(name, angles)], "conv", sep="."))
# }
# group_name <- "Left front leg - Right middle leg"
# for (name in c("LF", "RM")){
#    regressor_groups[[group_name]] <- append(regressor_groups[[group_name]], paste(angles[grepl(name, angles)], "conv", sep="."))
# }
# group_name <- "Left front leg - Right hind leg"
# for (name in c("LF", "RH")){
#    regressor_groups[[group_name]] <- append(regressor_groups[[group_name]], paste(angles[grepl(name, angles)], "conv", sep="."))
# }
# group_name <- "Left front leg - Left middle leg"
# for (name in c("LF", "LM")){
#    regressor_groups[[group_name]] <- append(regressor_groups[[group_name]], paste(angles[grepl(name, angles)], "conv", sep="."))
# }
# group_name <- "Left front leg - Left hind leg"
# for (name in c("LF", "LH")){
#    regressor_groups[[group_name]] <- append(regressor_groups[[group_name]], paste(angles[grepl(name, angles)], "conv", sep="."))
# }
# group_name <- "Left middle leg - Right front leg"
# for (name in c("LM", "RF")){
#    regressor_groups[[group_name]] <- append(regressor_groups[[group_name]], paste(angles[grepl(name, angles)], "conv", sep="."))
# }
# group_name <- "Left middle leg - Right middle leg"
# for (name in c("LM", "RM")){
#    regressor_groups[[group_name]] <- append(regressor_groups[[group_name]], paste(angles[grepl(name, angles)], "conv", sep="."))
# }
# group_name <- "Left middle leg - Right hind leg"
# for (name in c("LM", "RH")){
#    regressor_groups[[group_name]] <- append(regressor_groups[[group_name]], paste(angles[grepl(name, angles)], "conv", sep="."))
# }
# group_name <- "Left middle leg - Left hind leg"
# for (name in c("LM", "LH")){
#    regressor_groups[[group_name]] <- append(regressor_groups[[group_name]], paste(angles[grepl(name, angles)], "conv", sep="."))
# }
# group_name <- "Left hind leg - Right front leg"
# for (name in c("LH", "RF")){
#    regressor_groups[[group_name]] <- append(regressor_groups[[group_name]], paste(angles[grepl(name, angles)], "conv", sep="."))
# }
# group_name <- "Left hind leg - Right middle leg"
# for (name in c("LH", "RM")){
#    regressor_groups[[group_name]] <- append(regressor_groups[[group_name]], paste(angles[grepl(name, angles)], "conv", sep="."))
# }
# group_name <- "Left hind leg - Right hind leg"
# for (name in c("LH", "RH")){
#    regressor_groups[[group_name]] <- append(regressor_groups[[group_name]], paste(angles[grepl(name, angles)], "conv", sep="."))
# }

## print(regressor_groups)


##---------------------------------------------------##


print('start outputing GLM results')



results = data.frame()
coefficients_df = data.frame()
decay_times_df = data.frame()

# for (path in Sys.glob(paste(root_dir,"Ascending_neuron_screen_analysis_pipeline/output/Fig2_S4-GLM_jangles_legs_beh_DFF/behavior_prediction_paper_original_version/glm_input_files/[SRM]*.csv", sep=""))){
for (path in Sys.glob(paste(root_dir,"Ascending_neuron_screen_analysis_pipeline/output/Fig2_S4-GLM_jangles_legs_beh_DFF/glm_input_files/[SRM]*.csv", sep=""))){
    genotype = tools::file_path_sans_ext(basename(path))
    print('')
    print('##################################################')
    print(genotype)
    print('##################################################')

    complete_df <- read.csv.with.nan(path)
    
    complete_df$grooming <- (complete_df$antennal_grooming | complete_df$eye_grooming | complete_df$foreleg_grooming)
    
    complete_df$Genotype <- genotype
    complete_df <- complete_df[complete_df$dFF_processing == "raw" & complete_df$Regressor_processing == "raw", ]
    
    if (length(unique(complete_df$Fly)) != 1){
        print("more than one fly")
        print(unique(complete_df["Fly"]))
    }
    
    for (roi in unique(complete_df$ROI)){
        results_roi <- data.frame()
        df <- complete_df[complete_df$ROI == roi,]
        
        df$fold <- get_folds(df, behaviours)

        df <- apply_filter_to_trials(df, "dFF", moving_average)
        
        for (regressor in all_regressors){
            parameters = find_best_crf_parameters(df, regressor, possible_crf_parameters, non_negative_regressors, standardize, standardize.response)
            a <- parameters["a"]
            b <- parameters["b"]
            df <- convolve_with_crf(df, regressor, a, b)
            t_half <- get_half_life_time(a, b)
            current_observation <- data.frame(genotype, roi, regressor, t_half) 
            names(current_observation) <- c("Genotype", "ROI", "Regressor", "Decay.time")
            decay_times_df <- rbind(decay_times_df, current_observation)
        }
        all_regressors_conv <- paste(all_regressors, "conv", sep=".")
        
        for (fold in 1:10){
            test_data <- data.frame(df[df$fold == fold,])
            train_data <- data.frame(df[df$fold != fold,])
            
            train_mean <- mean(train_data$dFF)
            train_sd <- sd(train_data$dFF)
            train_max <- quantile(train_data$dFF, 0.995)
            normalized_train_data <- data.frame(train_data)
            normalized_test_data <- data.frame(test_data)
            normalized_train_data$dFF <- normalized_train_data$dFF / train_max
            normalized_test_data$dFF <- normalized_test_data$dFF / train_max
            test_data <- normalized_test_data
            train_data <- normalized_train_data
            
            lambda <- estimate_lambda(train_data, all_regressors_conv, behaviours, non_negative_regressors, standardize, standardize.response, intercept=intercept)
            complete_results <- model_function(train_data, test_data, all_regressors_conv, non_negative_regressors, lambda, standardize=standardize, standardize.response=standardize.response, intercept=intercept)
            complete_R2 <- complete_results[["adj.r.squared"]]
            f_p_value <- complete_results[["F p-value"]]
            

            coefficients_results <- model_function(normalized_train_data, normalized_test_data, all_regressors_conv, non_negative_regressors, lambda, standardize=standardize, standardize.response=standardize.response, intercept=intercept)
            coefficients <- coefficients_results[["coefficients"]]
            current_observation <- data.frame(genotype, roi, fold, complete_results[["r.squared"]], complete_results[["adj.r.squared"]], complete_results[["F p-value"]], lambda) 
            names(current_observation) <- c("Genotype", "ROI", "Fold", "r.squared", "adj.r.squared", "F p-value", "lambda")
            
            current_coeff <- cbind(current_observation, as.data.frame(coefficients))
            coefficients_df <- rbind(coefficients_df, current_coeff)

            n_repetitions <- 1
            #n_repetitions <- 5
            for (i in 1:n_repetitions){
                print(paste("Repetition:", i))
                for (group_name in names(regressor_groups)){
                    regressors <- regressor_groups[[group_name]]

                    current_repetition <- data.frame(current_observation)
                    current_repetition["Regressor"] <- group_name

                    shuffled_train_data <- shuffle_regressor(train_data, regressors)
                    shuffled_test_data <- shuffle_regressor(test_data, regressors)
                    
                    # Unique explained variance
                    complete_results <- model_function(shuffled_train_data, shuffled_test_data, all_regressors_conv, non_negative_regressors, lambda, standardize=standardize, standardize.response=standardize.response, intercept=intercept)
                    current_repetition[["adj.r.sq.w.o.explained.variance"]] <- complete_results[["adj.r.squared"]]
                    current_repetition[["r.sq.w.o.explained.variance"]] <- complete_results[["r.squared"]]

                    # All explained variance
                    shuffle_all_but_train_data <- shuffle_all_but_regressor(train_data, regressors)
                    shuffle_all_but_test_data <- shuffle_all_but_regressor(test_data, regressors)
                    complete_results <- model_function(shuffle_all_but_train_data, shuffle_all_but_test_data, all_regressors_conv, non_negative_regressors, lambda, standardize=standardize, standardize.response=standardize.response, intercept=intercept)
                    current_repetition[["adj.r.sq.only.explained.variance"]] <- complete_results[["adj.r.squared"]]
                    current_repetition[["r.sq.only.explained.variance"]] <- complete_results[["r.squared"]]
                    results_roi <- rbind(results_roi, current_repetition)
                }
            }
            results <- rbind(results, results_roi)
        }
    }
}

##-------Choose the corresponding output filename-------##

write.csv(results, paste(folder, "lm_results.csv", sep=""))
write.csv(coefficients_df, paste(folder, "coeff_results.csv", sep=""))
write.csv(decay_times_df, paste(folder, "decay_times_results.csv", sep=""))

# write.csv(results, paste(folder, "lm_results_angles.csv", sep=""))
# write.csv(coefficients_df, paste(folder, "coeff_results_angles.csv", sep=""))
# write.csv(decay_times_df, paste(folder, "decay_times_results_angles.csv", sep=""))

# write.csv(results, paste(folder, "lm_results_angles_legs.csv", sep=""))
# write.csv(coefficients_df, paste(folder, "coeff_results_angles_legs.csv", sep=""))
# write.csv(decay_times_df, paste(folder, "decay_times_results_angles_legs.csv", sep=""))

# write.csv(results, paste(folder, "lm_results_angles_leg_pairs.csv", sep=""))
# write.csv(coefficients_df, paste(folder, "coeff_results_angles_leg_pairs.csv", sep=""))
# write.csv(decay_times_df, paste(folder, "decay_times_results_angles_leg_pairs.csv", sep=""))

##------------------------------------------------------##
