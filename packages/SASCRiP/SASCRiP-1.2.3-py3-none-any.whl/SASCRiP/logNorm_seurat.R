# This R script contains the code to run NormalizeData
# which will be run through python

# required packages
library(tidyverse)
library(Seurat)
library(Matrix)

# Pre-defined R functions

# Convert the values in a list to their correct data type
# .. given the data type informations as a character vector
convert_data_type <- function(data_type_info_vect, list_of_values) {

	# Convert all argument values from the list_of_values list into their correct data type
	for ( number in seq(1, length(list_of_values)) ) {
		# string to correct data type
		if ( data_type_info_vect[number] == "num" ) {
			list_of_values[number] <- as.double(list_of_values[number])

		} else if ( data_type_info_vect[number] == "num_vect" ) {
			list_of_values[number] <- list(c(as.double(unlist(strsplit(unlist(list_of_values[number],
				use.names = FALSE),
			split = ",")))))

		} else if ( data_type_info_vect[number] == "char_vect" ) {
			list_of_values[number] <- list(c(unlist(strsplit(unlist(list_of_values[number],
				use.names = FALSE),
			split = ","))))

		} else if ( data_type_info_vect[number] == "logical" ) {
			list_of_values[number] <- as.logical(list_of_values[number])

		} else if ( data_type_info_vect[number] == "log_vect" ) {
			list_of_values[number] <- list(c(as.logical(unlist(strsplit(unlist(list_of_values[number],
				use.names = FALSE),
			split = ",")))))

		} else if ( data_type_info_vect[number] == "expression" ) {
			list_of_values[number] <- eval(parse(text = list_of_values[number]))

		} else if ( data_type_info_vect[number] == "expr_vect" ) {
			expr_vect <- c()
			for ( expression in parse(text = unlist(strsplit(unlist(list_of_values[number],
				use.names = FALSE),
			split = ","))) ) {
				expr_vect <- c(expr_vect, eval(expression))
			}
			list_of_values[number] <- list(c(expr_vect))

		} else if ( data_type_info_vect[number] == "list" ) {
			list_of_values[number] <- list(c(as.list(unlist(strsplit(unlist(list_of_values[number],
				use.names = FALSE),
			split = ",")))))

		} else if ( data_type_info_vect[number] == "NULL" ) {
			list_of_values[number] <- list(as.null(list_of_values[number]))
		}

	}
  return(list_of_values)
}

# General R function to load an RData file using a specified object name
loadRData <- function(filename) {
  load(filename)
  get(ls()[ls() != "filename"])
}

####################################################################################
# R function to replace the ENSEMBL IDs with hgnc gene names within a Seurat object
####################################################################################
ensg_to_hgnc <- function(
  ensg_gname_path,
  read_in_seurat_object,
  sample_ID
){
  print("Seurat object contains ENSEMBL gene names")
  # Set the path to the ensg_gname.tsv file
  print("Looking for tsv file containing ENSG names and HGNC gene symbols")
  # read in the ensg_gname.tsv file
  ensg_gname <- read_tsv(ensg_gname_path, col_names = FALSE)
  # Add colnames to the ensg_gname file
  colnames(ensg_gname) <- c("ENSEMBL_ID", "gene_name")
  # Assign read_in_seurat_object to sample_ID_srt
  sample_ID_srt <- read_in_seurat_object
  # Update Seurat object if saved as an old seurat object
  sample_ID_srt <- UpdateSeuratObject(sample_ID_srt)
  # Generate the dataframe that will be used to match and replace the ENSEMBL IDs
  pmatch_output <- data.frame(pmatch(ensg_gname$ENSEMBL_ID, rownames(sample_ID_srt@assays[["RNA"]]@counts)))
  colnames(pmatch_output) <- "gene_match"
  pmatch_output$match_index <- rownames(pmatch_output)
  pmatch_output <- pmatch_output[order(pmatch_output$gene_match), ]
  pmatch_output <- filter(pmatch_output, !is.na(gene_match))
  # Match and replace the ENSEMBL IDs in the relevant slots in the seurat object with the hgnc gene symbol
  print("Replacing ENSG names with corresponding HGNC gene symbols")
  rownames(sample_ID_srt@assays[["RNA"]]@counts) <- ensg_gname$gene_name[as.numeric(pmatch_output$match_index)]
  rownames(sample_ID_srt@assays[["RNA"]]@data) <- ensg_gname$gene_name[as.numeric(pmatch_output$match_index)]
  # Return the Seurat object with hgnc symbols as rownames
  return(sample_ID_srt)
}

# Read in and check the seurat object
read_check_srt <- function(
  seurat_object,
  sample_ID
){
  # Read in the saved seurat object
  if (endsWith(seurat_object, ".rds") == TRUE | endsWith(seurat_object, "RDS") == TRUE) {
    sample_ID_srt <- readRDS(file = seurat_object)
  } else {
    sample_ID_srt <- loadRData(seurat_object)
  }
  # Update Seurat object if saved as an old seurat object
  sample_ID_srt <- UpdateSeuratObject(sample_ID_srt)
  # Check if rownames use hgnc symbols or ENSEMBL IDs - change to hgnc symbol if ENSEMBL IDs are used
  # if (startsWith(rownames(sample_ID_srt@assays[["RNA"]]@counts)[1], "ENSG") == TRUE) {
  #   sample_ID_srt <- ensg_to_hgnc(ensg_gname_path, seurat_object, sample_ID)
  # }
  # Remove cell barcodes with counts of 0
  sample_ID_srt <- subset(sample_ID_srt, subset = nCount_RNA > 0)
  # Check if the mito.percent column is in the meta.data slot of the Seurat object
  if ("mito.percent" %in% colnames(sample_ID_srt@meta.data)) {
    sample_ID_srt <- sample_ID_srt
  } else {
    sample_ID_srt[['mito.percent']] <- PercentageFeatureSet(sample_ID_srt, pattern = '^MT-')
  }
  return(sample_ID_srt)
}

######################################################################
# Convert information from the Seurat object into a mtx count matrix
######################################################################
srt_count_mtx <- function(
  read_in_seurat_object,
  sample_ID,
  output_folder
){
  print("Converting Seurat Object to an mtx matrix")
  sample_ID_srt <- read_in_seurat_object
  sample_ID_sparse <- as.sparse(GetAssayData(sample_ID_srt, slot = 'counts'))
  writeMM(sample_ID_sparse, sprintf('%s/%s_normalised_matrix/matrix.mtx', output_folder, sample_ID))
  sample_ID_sparse_rows <- rownames(sample_ID_sparse)
  sample_ID_sparse_cols <- colnames(sample_ID_sparse)
  write.table(sample_ID_sparse_rows, file = sprintf('%s/%s_normalised_matrix/genes.tsv', output_folder, sample_ID), row.names = FALSE, col.names = FALSE, quote = FALSE)
  write.table(sample_ID_sparse_cols, file = sprintf('%s/%s_normalised_matrix/barcodes.tsv', output_folder, sample_ID), row.names = FALSE, col.names = FALSE, quote = FALSE)
}

######################################################################
# Convert information from the Seurat object into a mtx log count matrix
######################################################################
srt_log_mtx <- function(
  read_in_seurat_object,
  sample_ID,
  output_folder
){
  print("Converting Seurat Object to an mtx matrix")
  sample_ID_srt <-read_in_seurat_object
  sample_ID_sparse <- as.sparse(GetAssayData(sample_ID_srt, slot = 'data'))
  writeMM(sample_ID_sparse, sprintf('%s/%s_log_normalised_matrix/matrix.mtx', output_folder, sample_ID))
  sample_ID_sparse_rows <- rownames(sample_ID_sparse)
  sample_ID_sparse_cols <- colnames(sample_ID_sparse)
  write.table(sample_ID_sparse_rows, file = sprintf('%s/%s_log_normalised_matrix/genes.tsv', output_folder, sample_ID), row.names = FALSE, col.names = FALSE, quote = FALSE)
  write.table(sample_ID_sparse_cols, file = sprintf('%s/%s_log_normalised_matrix/barcodes.tsv', output_folder, sample_ID), row.names = FALSE, col.names = FALSE, quote = FALSE)
}

# All arguments input in Bash to be saved to the args list
args <- commandArgs(TRUE)

# Define all variables from bash arguments
seurat_object <- args[1] # Path to the filtered seurat object
sample_ID <- args[2]
output_directory_path <- args[3]
ouput_log_matrix <- as.logical(args[4])
ouput_count_matrix <- as.logical(args[5])
#is_add_args <- as.logical(args[7]) - not used here
#data_type_information <- args[8] - not used here
#add_args_list <- args[9] = not used here

# Read in the filtered Seurat Object
sample_ID_srt <- read_check_srt(seurat_object, sample_ID)

# Run the NormalizeData seurat function with the arguments given here
sample_ID_srt <- NormalizeData(
        sample_ID_srt
)
# Find variable features using the standardized variance
sample_ID_srt <- FindVariableFeatures(
        sample_ID_srt
) # The assay used here will be the "RNA" assay

# Save the normalised Seurat object to rds file
saveRDS(
  sample_ID_srt,
  file = sprintf("%s/%s_logNorm.rds", output_directory_path, sample_ID)
)

if ( ouput_log_matrix == TRUE ) {
	srt_log_mtx(
		sample_ID_srt,
		sample_ID,
		output_directory_path
	)
}

if ( ouput_count_matrix == TRUE ) {
	srt_count_mtx(
		sample_ID_srt,
		sample_ID,
		output_directory_path
	)
}
