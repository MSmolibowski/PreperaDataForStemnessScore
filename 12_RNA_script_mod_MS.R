library(gelnet)
library(dplyr)
library(biomaRt)
library(synapser)
synLogin("login", "password")


genes2hugo <- function( v, srcType = "ensembl_gene_id" )
{
    ## Retrieve the EMSEMBL -> HUGO mapping
    ensembl <- biomaRt::useMart( "ENSEMBL_MART_ENSEMBL", host="www.ensembl.org", dataset="hsapiens_gene_ensembl" )
    ID <- biomaRt::getBM( attributes=c(srcType, "hgnc_symbol"), filters=srcType, values=v, mart=ensembl )
    
    ## Make sure there was at least one mapping
    if( nrow(ID) < 1 ) top( "No IDs mapped successfully" )
    
    ## Drop empty duds
    j <- which( ID[,2] == "" )
    if( length(j) > 0 ) ID <- ID[-j,]
    stopifnot( all( ID[,1] %in% v ) )
    
    ID
}


main.train <- function( fnOut = "C:\\Users\\mikol\\Desktop\\R skrypt AnalizaMO\\PanCanStem_Web\\Rmardown\\data\\results\\train_res\\pcbc-stemsig.tsv", fnGenes = NULL )
{
    fnOut = "C:\\Users\\mikol\\Desktop\\Stemness Score\\Skrypt do Stemness Score\\PanCanStem_Web\\Rmardown\\data\\train_data\\train_res\\pcbc-stemsig.tsv"
    fnGenes = NULL
    
    ## Load RNAseq data
    #synRNA <- synGet( "syn2701943", downloadLocation = "/data/PCBC" )
    synRNA <- "C:\\Users\\mikol\\Desktop\\Stemness Score\\Skrypt do Stemness Score\\PanCanStem_Web\\Rmardown\\data\\train_data\\rnaseq_norm.tsv"
    
    #synRNA <- read.csv2(file.choose(), sep = '\t') #load traning data
    
    
    X <- read.delim( synRNA ) %>%
        tibble::column_to_rownames( "tracking_id" ) %>%
        as.matrix()
    
    ## Retrieve metadata
    
    synMeta <- synTableQuery( "SELECT UID, Diffname_short FROM syn3156503" )
    filepath <- synMeta$filepath
    synMeta <- read.delim(synMeta$filepath, sep = ',')
    
    Y <- synMeta %>%
        mutate( UID = gsub("-", ".", UID) ) %>%
        tibble::column_to_rownames( "UID" )
    
    ## Retrieve the labels from the metadata
    
    X_colnames <- colnames(X)
    Y_colnames <- row.names(Y)
    X_colnmb <- ncol(X)
    
    y <- data.frame(matrix(ncol = X_colnmb, nrow = 1))
    colnames(y) <- X_colnames
    
    for (x in X_colnames)                       #(MS) creating table with col names from X and values from Y
    {
        if (x %in% Y_colnames)
        {
            y[x] = Y[x, 'Diffname_short']
        }
    }
    
    
    ## Fix the missing labels by hand
    y["SC11.014BEB.133.5.6.11"] <- "EB"
    y["SC12.039ECTO.420.436.92.16"] <- "ECTO"
    
    ## Drop the splice form ID from the gene names
    v <- strsplit( rownames(X), "\\." ) %>% lapply( "[[", 1 ) %>% unlist()
    rownames(X) <- v
    
    ## Map Ensembl IDs to HUGO
    V <- genes2hugo( rownames(X) )
    X <- X[V[,1],]
    rownames(X) <- V[,2]
    
    ## Reduce the gene set to the provided list (if applicable)
    if( is.null( fnGenes ) == FALSE )
    {
        vGenes <- read.delim( fnGenes, header=FALSE ) %>% as.matrix() %>% drop()
        VE <- genes2hugo( vGenes, "entrezgene" )
        X <- X[intersect( rownames(X), VE[,2] ),]
    }
    
    ## Mean-center the data
    m <- apply( X, 1, mean )
    X <- X - m
    
    ## Identify stem cell samples
    j <- which( y == "SC" )
    X.tr <- X[,j]
    X.bk <- X[,-j]
    
    ## Train a one-class model
    mm <- gelnet( t(X.tr), NULL, 0, 1 )
    print(mm$w)
    
    ## Store the signature to a file
    write.table(mm$w, file = fnOut, sep = "\t", quote = FALSE, col.names = FALSE)
    
    ## Perform leave-one-out cross-validation
    auc <- c()
    for( i in 1:ncol(X.tr) )
    {
        ## Train a model on non-left-out data
        X1 <- X.tr[,-i]
        m1 <- gelnet( t(X1), NULL, 0, 1 )
        
        ## Score the left-out sample against the background
        s.bk <- apply( X.bk, 2, function(z) {cor( m1$w, z, method="sp" )} )
        s1 <- cor( m1$w, X.tr[,i], method="sp" )
        
        ## AUC = P( left-out sample is scored above the background )
        auc[i] <- sum( s1 > s.bk ) / length(s.bk)
        cat( "Current AUC: ", auc[i], "\n" )
        cat( "Average AUC: ", mean(auc), "\n" )
    }
    
    return(auc)
}


main.predict <- function()
{
    #--------------MS--------------------
    #set
    dataFolderIn <- "CzerniakReadyForStemnesScore"                    #name of folder where you store your data
    folder_path <- paste0("C:\\Users\\mikol\\Desktop\\Analizy Bioinformatyczne MO\\StemnesScoreAnalysis\\StemnesPrepareData\\data\\Czerniak\\",dataFolderIn) #path to the folder where data are stored
    files <- dir(folder_path) #files names in folder
    
    #----------
    for(fileName in files)
    {
     
      #out data used in analys path
      ourDataPath <- "C:\\Users\\mikol\\Desktop\\Analizy Bioinformatyczne MO\\StemnesScoreAnalysis\\StemnesPrepareData\\data\\Czerniak\\" #same path as folder_path
      ourDataPath <- paste0(ourDataPath, dataFolderIn,"\\", fileName)

      #output res path
      dataFolderOUT <- paste0(dataFolderIn,"_res")  #create res folder name using folder name stored in dataFolderIn
      resultFolderPath <- "C:\\Users\\mikol\\Desktop\\Analizy Bioinformatyczne MO\\StemnesScoreAnalysis\\PanCanStem_Web\\Rmardown\\data\\results\\"   #path to folder with results
      resultFolderPath <- paste0(resultFolderPath,dataFolderOUT, "\\res_", fileName) #create finall path to folder with results
      
      #-------------------------
      #trained
      fnSig <- "C:\\Users\\mikol\\Desktop\\Analizy Bioinformatyczne MO\\StemnesScoreAnalysis\\PanCanStem_Web\\Rmardown\\data\\train_data\\train_res\\pcbc-stemsig.tsv"
      
      ## Load the signature
      w <- read.delim(fnSig, header=FALSE, row.names=1 ) %>% as.matrix() %>% drop()
      
      
      
      ## Reduces HUGO|POSITION gene IDs to just HUGO
      f <- function( v ) unlist( lapply( strsplit( v, "\\|" ), "[[", 1 ) )
      
      #s <- synGet( "syn4976369", downloadLocation = "/data/pancan" )
      
      
      X <- read.delim( ourDataPath, as.is=TRUE, check.names=FALSE ) %>%	## Read the raw values      
        filter( !grepl( "\\?", gene_id ) ) %>%		## Drop genes with no mapping to HUGO
        mutate( gene_id = f( gene_id ) ) %>%		## Clip gene ids to HUGO
        filter( gene_id %in% names(w) )			## Reduce to the signature's gene set
      
      ## SLC35E2 has multiple entries with the same HUGO id
      ## Keep the first entry only
      j <- grep( "SLC35E2", X[,1] )
      if( length(j) > 1 )
        X <- X[-j[-1],]
      
      ## Convert to a matrix
      rownames(X) <- NULL
      X <- X %>% tibble::column_to_rownames( "gene_id" ) %>% as.matrix()
      
      ## Reduce the signature to the common set of genes
      stopifnot( all( rownames(X) %in% names(w) ) )
      w <- w[ rownames(X) ]
      
      ####### Score via Spearman correlation
      s <- apply( X, 2, function(z) {cor( z, w, method = "sp", use = "complete.obs" )} )
      
      ## Scale the scores to be between 0 and 1
      
      s <- s - min(s)
      s <- s / max(s)
      
      file.create(resultFolderPath)
      write.table(cbind(s), file = resultFolderPath, sep = "\t", quote = FALSE, col.names = FALSE)
    }
    
}





