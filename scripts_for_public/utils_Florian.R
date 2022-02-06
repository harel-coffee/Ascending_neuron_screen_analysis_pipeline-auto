library(ggplot2)
library(glmnet)
library(caret)
library(plyr)
library(stringr)
library(tidyr)
library(grid)
library(scales)
library(tools)



# root_dir = "/mnt/data/CLC/"
root_dir=paste(file_path_as_absolute("../../"),"/", sep="")

# behaviour_colours <- c("Walking"="#e7298a", "Resting"="gray", "Antennal grooming"="#7570b3", "Eye grooming"="#66a61e", "Front leg grooming"="#e6ab02", "Pushing"="#1b9e77", "Rear leg grooming"="#d95f02", "Abdominal grooming"="#a6761d", "Proboscis extension"="#4A6DFF", "PE"="#4A6DFF", "CO2"="black")
behaviour_colours <- c("Forward walking"="deeppink1", "Backward walking"="seagreen2", "Resting"="gray", "Antennal grooming"="mediumpurple2", "Eye grooming"="#66a61e", "Front leg grooming"="#e6ab02", "Pushing"="#1b9e77", "Rear leg grooming"="#d95f02", "Abdominal grooming"="#a6761d", "Proboscis extension"="#4A6DFF", "PE"="#4A6DFF", "CO2"="black")
behaviour_colours <- c("Forward walking"="skyblue", "Backward walking"="springgreen", "Resting"="gray", "Antennal grooming"="orange", "Eye grooming"="hotpink", "Front leg grooming"="darkviolet", "Pushing"="blue", "Rear leg grooming"="khaki4", "Abdominal grooming"="yellowgreen", "Proboscis extension"="gold", "PE"="gold", "CO2"="black")


read.csv.with.nan <- function(path){
    df <- read.csv(path)
    # behaviours <- c("rest", "walking", "antennal_grooming", "eye_grooming", "foreleg_grooming", "hindleg_grooming", "abdominal_grooming", "PER_event", "pushing", "CO2")
    behaviours <- c("rest", "backward_walking", "forward_walking", "antennal_grooming", "eye_grooming", "foreleg_grooming", "hindleg_grooming", "abdominal_grooming", "PER_event", "pushing", "CO2")

    for (behaviour in behaviours){
        df[df[[behaviour]] == "", behaviour] = "False"
        df[is.na(df[[behaviour]]), behaviour] = "False"
        df[[behaviour]] <- as.logical(df[[behaviour]])
    }
    return(df)
}


plot_matrix <- function(df, value_col, row.order, scale_name, output_file, f_p_value_df, x_label, range, text_col, as_perc, justifications, ROI_label_angle){
    if (missing(x_label)){
        x_label <- ""
    }
    if (missing(range)){
        range <- c(min(df[, value_col]), max(df[, value_col]))
    }
    if (missing(ROI_label_angle)){
        ROI_label_angle <- 0
    }
    # Fix order of Genotype_ROI
    df.row.order <- unique(match(row.order, df$Genotype_ROI))
    df.row.order <- df.row.order[!is.na(df.row.order)]
    df$Genotype_ROI <- factor(df$Genotype_ROI, levels = df$Genotype_ROI[df.row.order])

    gal4s <- unique(df$Genotype[df.row.order])
    gal4_pos <- c()
    gal4_line_start <- c()
    gal4_line_stop <- c()
    for (gal4 in gal4s){
        gal4_pos <- c(gal4_pos, mean(which(df$Genotype[df.row.order] %in% gal4)))
        gal4_line_start <- c(gal4_line_start, min(which(df$Genotype[df.row.order] %in% gal4)))
        gal4_line_stop <- c(gal4_line_stop, max(which(df$Genotype[df.row.order] %in% gal4)))
    }
    gal4s <- lapply(gal4s, as.character)
    gal4_colours <- replicate(length(gal4s), "black")
    gal4_line_col <- replicate(length(gal4s), "black")
    gal4_line_col[seq(1, length(gal4_line_col), 2)] <- "#646464"
    gal4_colours[gal4s %in% c("SS29579", "SS51046", "SS42740")] <- behaviour_colours["Forward walking"]
    gal4_colours[gal4s %in% c("SS25469")] <- behaviour_colours["Eye grooming"]
    gal4_colours[gal4s %in% c("SS31232")] <- behaviour_colours["Proboscis extension"]
    gal4_colours[gal4s %in% c("SS27485")] <- behaviour_colours["Resting"]
    gal4_line_col[gal4s %in% c("SS29579", "SS51046", "SS42740")] <- behaviour_colours["Forward walking"]
    gal4_line_col[gal4s %in% c("SS25469")] <- behaviour_colours["Eye grooming"]
    gal4_line_col[gal4s %in% c("SS31232")] <- behaviour_colours["Proboscis extension"]
    gal4_line_col[gal4s %in% c("SS27485")] <- behaviour_colours["Resting"]
    gal4s <- str_pad(gal4s, max(unlist((lapply(gal4s, nchar)))), "right")
    
    if (!missing(f_p_value_df)){
        f_p_value_df.row.order <- unique(match(row.order, f_p_value_df$Genotype_ROI))
        f_p_value_df.row.order <- f_p_value_df.row.order[!is.na(f_p_value_df.row.order)]
    }

    if (! value_col %in% names(df)){
        print(colnames(df))
        stop(paste(value_col, "is not a column of df"))
    }
    names(df)[names(df) == value_col] <- "value"
    if (missing(as_perc)){
        as_perc <- FALSE
    }
    if (as_perc){
        df$value <- df$value * 100
        range <- range * 100
    }
    
    # Mark selected lines
    selected_lines <- "(SS29579 [0123]|SS51046 [01]|SS42740 [01]|SS25469 [01]|SS31232 [01]|SS27485 [023])"
    faces <- ifelse(
                    grepl(
                          selected_lines,
                          levels(df$Genotype_ROI),
                         ),
                    "bold",
                    "plain"
                   )
    if (length(unique(faces)) == 1){
        selected_lines <- "(SS29579|SS34574|SS42740|SS25469|SS31232|SS27485)"
        faces <- ifelse(
                        grepl(
                              selected_lines,
                              levels(df$Genotype_ROI),
                             ),
                        "bold",
                        "plain"
                       )
    }

    n_rows <- nlevels(droplevels(as.factor(df$Regressor)))
    
    if (missing(justifications)){
        justifications <- c()
    }
    if (! "neuron_num_hjust" %in% names(justifications)){
        justifications <- c(justifications, neuron_num_hjust=1.1)
    }
    if (! "neuron_num_vjust" %in% names(justifications)){
        justifications <- c(justifications, neuron_num_vjust=-1.5/34*n_rows + 1000/34)
    }
    if (! "driver_line_hjust" %in% names(justifications)){
        justifications <- c(justifications, driver_line_hjust=1.1)
    }
    if (! "driver_line_vjust" %in% names(justifications)){
        justifications <- c(justifications, driver_line_vjust=5.8)
    }
    if (! "gal4_hjust" %in% names(justifications)){
        justifications <- c(justifications, gal4_hjust=2.3)
    }
    if (! "gal4_vjust" %in% names(justifications)){
        justifications <- c(justifications, gal4_vjust=0.51)
    }
    if (! "gal4_line_y" %in% names(justifications)){
        justifications <- c(justifications, gal4_line_y=-3.2/34 * n_rows + 15.4/34)
    }
    if (! "p_value_hjust" %in% names(justifications)){
        justifications <- c(justifications, p_value_hjust=1.1)
    }
    if (! "p_value_vjust" %in% names(justifications)){
        justifications <- c(justifications, p_value_vjust=0.8/34 * n_rows - 2.5)
    }
    if (! "star_hjust" %in% names(justifications)){
        justifications <- c(justifications, star_hjust=1/34 * n_rows + (-76/34))
    }
    if (! "star_vjust" %in% names(justifications)){
        justifications <- c(justifications, star_vjust=0.8)
    }

    if ("ROI" %in% names(df)){
        x_labels <- as.vector(df$ROI)
        names(x_labels) <- as.vector(df$Genotype_ROI)
    } else {
        x_labels <- rep("", length(as.vector(df$Genotype_ROI)))
        names(x_labels) <- as.vector(df$Genotype_ROI)
    }

    levels <- c(
                "LH TiTa pitch", "RH TiTa pitch", "LH FTi pitch", "RH FTi pitch", "LH CTr roll", "RH CTr roll", "LH CTr pitch", "RH CTr pitch", "LH ThC roll", "RH ThC roll", "LH ThC pitch", "RH ThC pitch", "LH ThC yaw", "RH ThC yaw",
                "LM TiTa pitch", "RM TiTa pitch", "LM FTi pitch", "RM FTi pitch", "LM CTr roll", "RM CTr roll", "LM CTr pitch", "RM CTr pitch", "LM ThC roll", "RM ThC roll", "LM ThC pitch", "RM ThC pitch", "LM ThC yaw", "RM ThC yaw",
                "LF TiTa pitch", "RF TiTa pitch", "LF FTi pitch", "RF FTi pitch", "LF CTr roll", "RF CTr roll", "LF CTr pitch", "RF CTr pitch", "LF ThC roll", "RF ThC roll", "LF ThC pitch", "RF ThC pitch", "LF ThC yaw", "RF ThC yaw",
                "Roll", "Yaw", "Pitch",
                "Proboscis extension", "Rear leg grooming", "Abdominal grooming", "Front leg grooming", "Antennal grooming", "Eye grooming", "Resting",  "Pushing", "Backward walking", "Forward walking",
                "Abdominal ganglion", "Haltere tectulum", "Wing tectulum", "Neck tectulum", "Intermediate tectulum", "Lower tectulum", "Accessory mesothoracic neuromere", "Metathoracic neuromere", "Mesothoracic neuromere", "Prothoracic neuromere",
                "Other", "GNG", "AVLP",
                "T3","T2","T1")
                #"CO\u0032 puff", "backward walking", "Proboscis extension", "Pushing", "Abdominal grooming", "Rear leg grooming", "Front leg grooming", "Antennal grooming", "Eye grooming", "grooming", "Resting", "Forward walking")
    additional_levels <- as.vector(unlist(unique(df[!(df$Regressor %in% levels), "Regressor"])))
    df$Regressor <- factor(df$Regressor, levels=c(additional_levels, levels))
    indices <- match(sort(unique(df$Regressor)), names(behaviour_colours))
    modified_behaviour_colours <- behaviour_colours
    y_tick_label_colours <- modified_behaviour_colours[indices]
    y_tick_label_colours <- replace_na(y_tick_label_colours, "black")


    size_factor <- 2.134
    ## dodgerblue ##red ##black
    p <- ggplot(data=df, aes(x=Genotype_ROI, y=Regressor, fill=value)) +
        geom_tile(colour="white", stat="identity") +
        scale_fill_gradient2(low=muted("red"), mid="white", high=muted("black"), midpoint=0, na.value="white", limits=range, space = "Lab") +
        scale_x_discrete(labels=x_labels) +
        theme(panel.grid.major = element_blank(),
              panel.grid.minor = element_blank(),
              panel.background = element_blank(),
              panel.border = element_rect(colour="black", fill=NA, size=0.25 / size_factor),
              axis.text.x = element_text(face=faces, family="Arial", colour="black", size=2, angle=ROI_label_angle),
              axis.text.y = element_text(family="Arial",
                                         colour=y_tick_label_colours,
                                         size=min(c(4, 42/n_rows))),
              axis.ticks = element_line(colour = "black", size=0.5 / size_factor),
              axis.ticks.length = unit(1.198, "pt"),
              text = element_text(family="Arial", colour = "black", size=6),
              legend.title=element_text(family="Arial", colour="black", size=4),
              legend.text=element_text(family="Arial", colour="black", size=4),
              legend.position="top"
             ) +

        guides(fill = guide_colourbar(title.position="bottom", barwidth=unit(90, "pt"), frame.colour="black", frame.linewidth=0.25 / 0.76, direction="horizontal", barheight = unit(3, "pt"), ticks.colour="black", ticks.linewidth=0.5 / 0.76, label.position="top")) +
        annotate(geom="text", x=1, hjust=justifications[["driver_line_hjust"]], y=1, vjust=justifications[["driver_line_vjust"]], label="Gal4 driver line", size=1, family="Arial") +
        annotate(geom="text", x=gal4_pos, hjust=justifications[["gal4_hjust"]], y=1, vjust=justifications[["gal4_vjust"]], label=gal4s, size=2/3, family="Arial", angle=90, colour=gal4_colours) +
        coord_cartesian(expand = FALSE, clip = "off") +
        labs(x=x_label, y="Behavioral regressor", fill=scale_name)
        
    if ("ROI" %in% names(df)){
        p <- p + 
        annotate(geom="text", x=1, hjust=justifications[["neuron_num_hjust"]], y=1, vjust=justifications[["neuron_num_vjust"]], label="Neuron (#)", size=1, family="Arial")
    }

    if (!missing(f_p_value_df)){
        p <- p +
        annotate(geom="text", x=1, hjust=justifications[["p_value_hjust"]], y=n_rows, vjust=justifications[["p_value_vjust"]], label="P-value", size=1, family="Arial") +
        annotate(geom = "text",
                 x = seq_len(nrow(f_p_value_df)),
                 hjust=justifications[["star_hjust"]],
                 y = n_rows,
                 vjust = justifications[["star_vjust"]],
                 label = f_p_value_df$Significance.stars[f_p_value_df.row.order],
                 size = 2/3,
                 angle = 90,
                 family="Arial"
                )
    }
    if (!missing(text_col)){
        names(df)[names(df) == text_col] <- "center_text"
        p <- p + geom_text(data=df, aes(label=center_text), size=2/3, angle=90, vjust=0.8, family="Arial")
    } 
    gal4_line_y <- justifications[["gal4_line_y"]]
    for (i in 1:length(gal4s)){
        p <- p + annotation_custom(grob=linesGrob(gp=gpar(col=gal4_line_col[i], lineend="square")),
                                   xmin=gal4_line_start[i]+0.1,
                                   xmax=gal4_line_stop[i] + 0.2, 
                                   ymin=gal4_line_y,
                                   ymax=gal4_line_y
                                  )
    }
    ggsave(output_file, height=3.6, width=15, scale=0.5, device=cairo_pdf, bg="transparent")
    # ggsave(output_file, device=cairo_pdf, scale=0.5, bg="transparent")
}


apply_filter_to_trials <- function(df, columns, filter){
    for (t in unique(df$Trial)){
        for (col in columns){
            df[df$Trial == t,][[col]] <- filter(df[df$Trial == t,][[col]])
        }
    }
    return(df)
}


moving_average <- function(x, n = 35){
    x <- append(rep(x[1], n), x)
    x <- append(x, rep(x[length(x)], n))
    x <- stats::filter(x, rep(1 / n, n), sides = 2)
    x <- x[-1:-n]
    x <- x[1:(length(x) - n)]
    return(x)
}


calcium_response_function <- function(t, a, b){
    y <- -exp(-a * t) + exp(-b * t)
    y <- y / sum(y)
}


convolve_with_crf <- function(df, regressors, a, b){
    for (trial in unique(df$Trial)){
        for (regressor in regressors){
            x <- as.numeric(df[df$Trial == trial, regressor])
            t <- as.numeric(df[df$Trial == trial, "Frame_times"])
            t <- t - min(t)
            t <- t[t < 10]
            crf <- calcium_response_function(t, a, b)
            df[df$Trial == trial, paste(regressor, "conv", sep=".")] <- convolve(x, rev(crf), type="open")[1:length(x) + 1]
        }
    }
    return(df)
}


find_best_crf_parameters <- function(df, regressor, possible_parameters, non_negative_regressors, standardize, standardize.response){
    max_var <- 0
    for (r in regressor){
        df[,r] <- as.numeric(df[,r])
        variance = var(df[,r])
        if (variance > max_var){
            max_var <- variance
        }
    }
    if (max_var == 0){
        return(c("a"=possible_parameters[1, "a"], "b"=possible_parameters[1, "b"]))
    }
    r_squared <- -2
    chosen_a <- NA
    chosen_b <- NA
    for (index in 1:nrow(possible_parameters)){
        convolved_df <- data.frame(df)
        a <- possible_parameters[index, "a"] 
        b <- possible_parameters[index, "b"]
        convolved_df <- convolve_with_crf(convolved_df, regressor, a, b)
        results <- model_function(convolved_df, convolved_df, paste(regressor, "conv", sep="."), non_negative_regressors,
                                     0,
                                     standardize,
                                     standardize.response)
        if (results$r.squared >= r_squared){
            r_squared <- results$r.squared
            chosen_a <- a
            chosen_b <- b
        }
    }
    return(c("a"=chosen_a, "b"=chosen_b))
}


get_folds <- function(data, regressors){
    regressor_col <- max.col(data[,regressors])
    folds <- createFolds(factor(regressor_col), k=10, list=FALSE)
}


model_function <- function(train_data, test_data, regressors, non_negative_regressors, lambda, standardize, standardize.response, negative_regressors, intercept, weights){
    if (missing(lambda)){
        lambda <- 0
    }
    if (missing(standardize)){
        standardize <- FALSE
    }
    if (missing(standardize.response)){
        standardize.response <- FALSE
    }
    if (missing(negative_regressors)){
        negative_regressors <- c()
    }
    if (missing(intercept)){
        intercept <- TRUE
    }
    if (missing(weights)){
        weights <- NULL
    }

    test_X_and_y <- get_X_and_y(test_data, regressors)
    X_test <- test_X_and_y[["X"]]
    y_test <- test_X_and_y[["y"]]
    
    train_X_and_y <- get_X_and_y(train_data, regressors)
    X_train <- train_X_and_y[["X"]]
    y_train <- train_X_and_y[["y"]]

    lower.limits <- rep(-Inf, length(regressors))
    lower.limits[regressors %in% non_negative_regressors] <- 0

    upper.limits <- rep(Inf, length(regressors))
    upper.limits[regressors %in% negative_regressors] <- 0
    
    fit <- glmnet(X_train, y_train, alpha=0, lambda=lambda, lower.limits=lower.limits, standardize=standardize, standardize.response=standardize.response, upper.limits=upper.limits, intercept=intercept, weights=weights)
    
    coefficients <- as.data.frame(as.matrix(coef(fit, s=lambda)))
    coefficients <- tibble::rownames_to_column(coefficients, "Regressor")
    names(coefficients)[names(coefficients) != "Regressor"] <- "Coefficient"

    yhat <- as.vector(predict(fit, newx=X_test, s=lambda))
    
    n <- length(y_test)
    p <- dim(X_test)[2]
    adj.r.squared <- get_adj_r_squared(y_test, yhat, n, p)
    r.squared <- get_r_squared(y_test, yhat)
    f_p_value <- get_F_p_value(y_test, yhat, n, p)
    return(list("adj.r.squared"=adj.r.squared, "r.squared"=r.squared, "coefficients"=coefficients, "F p-value"=f_p_value, "prediction"=yhat))
}


rename_behaviours <- function(df){
    old_names <- c("rest", "walking", "forward_walking", "backward_walking", "antennal_grooming", "eye_grooming", "foreleg_grooming", "hindleg_grooming", "abdominal_grooming", "PER_event", "pushing", "CO2", "Yaw", "Pitch", "Roll", "resting", "walking")
    old_names_conv <- paste(old_names, "conv", sep=".")
    new_names <- c("Resting", "Walking", "Forward walking", "Backward walking", "Antennal grooming", "Eye grooming", "Front leg grooming", "Rear leg grooming", "Abdominal grooming", "Proboscis extension", "Pushing", "CO\u2082 puff", "Yaw", "Pitch", "Roll", "Resting", "Walking")
    for (i in 1:length(old_names)){
        names(df)[names(df) == old_names[i]] <- new_names[i]
        names(df)[names(df) == old_names_conv[i]] <- new_names[i]
    }
    if ("Behaviour" %in% names(df)){
        df$Behaviour <- mapvalues(df$Behaviour, from=old_names, to=new_names)
        df$Behaviour <- mapvalues(df$Behaviour, from=old_names_conv, to=new_names)
    }
    if ("Regressor" %in% names(df)){
        df$Regressor <- mapvalues(df$Regressor, from=old_names, to=new_names)
        df$Regressor <- mapvalues(df$Regressor, from=old_names_conv, to=new_names)
    }
    return(df)
}


rename_angles <- function(df){
    old_names <- c(
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
    old_names_conv <- paste(old_names, "conv", sep=".")
    new_names <- c(
           "LF ThC yaw",     "LF ThC pitch",   "LF ThC roll",
           "LF CTr pitch",   "LF FTi pitch",   "LF CTr roll",
           "LF TiTa pitch",   "LM ThC yaw",     "LM ThC pitch",
           "LM ThC roll",    "LM CTr pitch",   "LM FTi pitch",
           "LM CTr roll", "LM TiTa pitch",   "LH ThC yaw",
           "LH ThC pitch",   "LH ThC roll",    "LH CTr pitch",
           "LH FTi pitch",   "LH CTr roll", "LH TiTa pitch",
           "RF ThC yaw",     "RF ThC pitch",   "RF ThC roll",
           "RF CTr pitch",   "RF FTi pitch",   "RF CTr roll",
           "RF TiTa pitch",   "RM ThC yaw",     "RM ThC pitch",
           "RM ThC roll",    "RM CTr pitch",   "RM FTi pitch",
           "RM CTr roll", "RM TiTa pitch",   "RH ThC yaw",
           "RH ThC pitch",   "RH ThC roll",    "RH CTr pitch",
           "RH FTi pitch",   "RH CTr roll", "RH TiTa pitch"
          )
    for (i in 1:length(old_names)){
        names(df)[names(df) == old_names[i]] <- new_names[i]
        names(df)[names(df) == old_names_conv[i]] <- new_names[i]
    }
    if ("Regressor" %in% names(df)){
        df$Regressor <- mapvalues(df$Regressor, from=old_names, to=new_names)
        df$Regressor <- mapvalues(df$Regressor, from=old_names_conv, to=new_names)
    }
    return(df)
}


plot_scatter <- function(df, variable, output_file, annotation_1, annotation_2, x_label, annotation_x, size){
    if (missing(annotation_1)){
        annotation_1 <- ""
    }
    if (missing(annotation_2)){
        annotation_2 <- ""
    }
    if (missing(x_label)){
        x_label <- ""
    }
    if (missing(annotation_x)){
        annotation_x <- 0
    }
    if (missing(size)){
        size <- c(4, 4)
    }
    names(df)[names(df) == variable] <- "variable"
    size_factor <- 2.134
    ggplot(df, aes(x=variable, y=dFF)) +
        geom_point(alpha=0.1, size=0.2, shape=16) +
        geom_smooth(method=lm, color="#1FBDC1", size=0.5 / size_factor) +
        annotate("text", x=annotation_x, y=max(df$dFF), label=annotation_1, colour="black", family="Arial", size=1.4059) +
        annotate("text", x=annotation_x, y=max(df$dFF)*0.8, label=annotation_2, colour="black", family="Arial", size=1.4059) +
        labs(x = x_label, y = "%\u0394F/F") +
        theme(panel.grid.major = element_blank(),
              panel.grid.minor = element_blank(),
              panel.background = element_rect(fill="transparent"),
              axis.line = element_line(colour = "black", size=0.5 / size_factor, lineend = "square"),
              text = element_text(family="Arial", colour = "black", size=6),
              axis.text = element_text(family="Arial", colour = "black", size=4),
              axis.ticks = element_line(colour = "black", size=0.5 / size_factor),
              axis.ticks.length = unit(1.522, "pt"),
              legend.title=element_text(family="Arial", colour="black", size=6),
              legend.text=element_text(family="Arial", colour="black", size=4)
             )
    ggsave(output_file, height=size[1], width=size[2], scale=0.25, device=cairo_pdf,   bg="transparent")
}


get_X_and_y <- function(data, regressors, response_var){
    if (missing(response_var)){
        response_var <- "dFF"
    }
    if (length(regressors) == 1){
        data["Intercept"] = 1
        regressors = c("Intercept", regressors)
    }
    X <- as.matrix(sapply(data[regressors], as.numeric))
    y <- as.vector(data[[response_var]])
    list("X"=X, "y"=y)
}


get_SST <- function(y){
    SST <- sum((y - mean(y)) ^ 2)
}


get_SSE <- function(y, yhat){
    SSE <- sum((y - yhat) ^ 2)
}


get_SSM <- function(y, yhat){
    SSM <- sum((yhat - mean(y)) ^ 2)
}


get_DFE <- function(n, p){
    DFE <- n - p
}


get_DFM <- function(p){
    DFM <- p - 1
}


get_r_squared <- function(y, yhat){
    SSE <- get_SSE(y, yhat)
    SST <- get_SST(y)
    r.squared <- 1 - SSE / SST
}


get_adj_r_squared <- function(y, yhat, n, p){
    r.squared <- get_r_squared(y, yhat)
    adj.r.squared <- 1 - (1 - r.squared) * ((n - 1) / (n - p))
}


get_F_p_value <- function(y, yhat, n, p){
    DFE <- get_DFE(n, p)
    DFM <- get_DFM(p)
    SSE <- get_SSE(y, yhat)
    SSM <- get_SSM(y, yhat)
    f <- (SSM / DFM) / (SSE / DFE)
    p.value <- pf(f, DFM, DFE, lower.tail = FALSE)
}


plot_predictions <- function(df, output_file, annotation_text_1, annotation_text_2, size){
    if (missing(annotation_text_1)){
        annotation_text_1 <- ""
    }
    if (missing(annotation_text_2)){
        annotation_text_2 <- ""
    }
    if (missing(size)){
        size <- c(2.7, 12.5)
    }
    first_line <- unique(df$Lines)[1]
    if (length(unique(df[df$Lines == first_line, "Frame_times"])) != nrow(df[df$Lines == first_line,])){
        stop("Frame times are not unique!")
    }
    df <- df[order(df$Lines, df$Frame_times),]
    for (line in unique(df$Lines)){
        df[df$Lines == line, "x1"] <- df[df$Lines == line, "Frame_times"]
        df[df$Lines == line, "x2"] <- df[df$Lines == line, "Frame_times"] + c(diff(df[df$Lines == line, "Frame_times"]),  mean(diff(df[df$Lines == line, "Frame_times"])))
        df[df$Lines == line, "y1"] <- max(df[df$Lines == line, "dFF"]) + 0.1 * (max(df[df$Lines == line, "dFF"]) - min(df[df$Lines == line, "dFF"]))
        df[df$Lines == line, "y2"] <- max(df[df$Lines == line, "dFF"]) + 0.2 * (max(df[df$Lines == line, "dFF"]) - min(df[df$Lines == line, "dFF"]))
        
        df[df$Lines == line, "y1_CO2"] <- df[df$Lines == line, "y2"]
        df[df$Lines == line, "y2_CO2"] <- df[df$Lines == line, "y1_CO2"] + (df[df$Lines == line, "y2"] - df[df$Lines == line, "y1"])
        
        df[df$Lines == line, "y1_PE"] <- df[df$Lines == line, "y2_CO2"]
        df[df$Lines == line, "y2_PE"] <- df[df$Lines == line, "y1_PE"] + (df[df$Lines == line, "y2"] - df[df$Lines == line, "y1"])
    }
    df$Behaviour[df$Behaviour == ""] <- NA
    df$Behaviour[df$Lines != first_line] <- NA
    df$Proboscis.extension.marker <- NA
    df$CO2.marker <- NA
    df[df[, "Proboscis extension"] > 0, "Proboscis.extension.marker"] <- "PE"
    df[df[, "CO\u2082 puff"] > 0, "CO2.marker"] <- "CO2"
    df$Proboscis.extension.marker[df$Lines != first_line] <- NA
    df$CO2.marker[df$Lines != first_line] <- NA
    
    annotation_x <- min(df$Frame_times) + 0.9 * (max(df$Frame_times) - min(df$Frame_times)) 
    annotation_y <- min(df$dFF) + 0.9 * (max(df$dFF) - min(df$dFF)) 
    annotation_y_2 <- min(df$dFF) + 0.1 * (max(df$dFF) - min(df$dFF)) 
    size_factor <- 2.134
    
    ggplot(data=df, aes(x=Frame_times, y=dFF, group=Lines)) +
        geom_rect(aes(xmin=x1, xmax=x2, ymin=y1, ymax=y2, fill=Behaviour)) +
        geom_rect(aes(xmin=x1, xmax=x2, ymin=y1_PE, ymax=y2_PE, fill=Proboscis.extension.marker)) +
        geom_rect(aes(xmin=x1, xmax=x2, ymin=y1_CO2, ymax=y2_CO2, fill=CO2.marker)) +
        scale_discrete_manual("fill", values=behaviour_colours,
                            na.translate=FALSE) +
        geom_line(aes(color=Lines), size = 0.5 / size_factor) +
        scale_color_manual(values=c("#000000", "#1FBDC1", "#808080")) +
        labs(x = "Time (s)", y = "%\u0394F/F") +
        annotate("text", x=annotation_x, y=annotation_y, label=annotation_text_1, family="Arial", colour="black", size=1.4059) +
        annotate("text", x=annotation_x, y=annotation_y_2, label=annotation_text_2, family="Arial", colour="black", size=1.4059) +
        theme(panel.grid.major = element_blank(),
              panel.grid.minor = element_blank(),
              panel.background = element_rect(fill="transparent"),
              axis.line = element_line(colour = "black", size=0.5 / size_factor, lineend = "square"),
              text = element_text(family="Arial", colour = "black", size=6),
              axis.text = element_text(family="Arial", colour = "black", size=4),
              axis.ticks = element_line(colour = "black", size=0.5 / size_factor),
              axis.ticks.length = unit(1.522, "pt"),
              legend.key.size = unit(0.2, "line"),
              legend.title=element_text(family="Arial", colour="black", size=6),
              legend.text=element_text(family="Arial", colour="black", size=4),
              )
    ggsave(output_file, height=size[1], width=size[2], scale=0.25, device=cairo_pdf)
}


get_half_life_time <- function(a, b){
    t <- seq(from=0, to=3, by=0.001)
    y <- calcium_response_function(t, a, b)    
    t_peak <- t[which.max(y)]
    y <- y - 0.5 * max(y)
    y[1:which.max(y)] <- Inf
    y <- abs(y)
    t_half <- t[which.min(y)] - t_peak
    return(t_half)
}


sem <- function(x){
    sd(x) / sqrt(length(x))
}


estimate_lambda <- function(data, regressors, behaviours, non_negative_regressors, standardize, standardize.response, response_var, negative_regressors, intercept, weights){
    if (missing(response_var)){
        response_var <- "dFF"
    }
    if (missing(negative_regressors)){
        negative_regressors <- c()
    }
    if (missing(intercept)){
        intercept <- TRUE
    }
    if (missing(weights)){
        weights <- NULL
    }
    data$fold <- get_folds(data, behaviours)

    X_and_y <- get_X_and_y(data, regressors, response_var)
    X <- X_and_y[["X"]]
    y <- X_and_y[["y"]]

    lower.limits <- rep(-Inf, length(regressors))
    lower.limits[regressors %in% non_negative_regressors] <- 0
    upper.limits <- rep(Inf, length(regressors))
    upper.limits[regressors %in% negative_regressors] <- 0
    fit <- cv.glmnet(X, y, foldid=data$fold, alpha=0, lower.limits=lower.limits, standardize=standardize, standardize.response=standardize.response, upper.limits=upper.limits, intercept=intercept, weights=weights)
    lambda <- fit$lambda.min
}


shuffle_regressor <- function(df, regressor){
    shuffled_df <- data.frame(df)
    for (r in names(shuffled_df)){
        if (any(grepl(r, regressor, fixed=TRUE))){
            shuffled_df[[r]] <- sample(shuffled_df[[r]])
        }
    }
    return(shuffled_df)
}


shuffle_all_but_regressor <- function(df, regressor){
    shuffled_df <- data.frame(df)
    for (r in names(shuffled_df)){
        if (any(grepl(r, regressor, fixed=TRUE)) || r == "Frame_times" || r == "dFF"){
            next
        }
        shuffled_df[[r]] <- sample(shuffled_df[[r]])
    }
    return(shuffled_df)
}


summarize_shuffeling_repetitions_results <- function(df){
    group_vars <- c("Genotype", "ROI", "Regressor", "Fold")
    group_vars <- intersect(group_vars, colnames(df))
    summarized_df <- df %>% group_by_at(group_vars) %>% summarize_at(vars(-group_cols()), list("mean"=mean, "sem"=sem))
}


summarize_cv_results <- function(df){
    group_vars <- c("Genotype", "ROI", "Regressor")
    group_vars <- intersect(group_vars, colnames(df))
    summarized_df <- df %>% group_by_at(group_vars) %>% summarize_at(vars(-group_cols(), -Fold), list("mean"=mean, "sem"=sem))
}
