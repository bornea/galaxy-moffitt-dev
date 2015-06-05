import os
import sys 
import time
from bs4 import BeautifulSoup
import lxml


file_locations_joined = sys.argv[1]
file_locations = file_locations_joined.split(",")
#Takes the .raw files as .dat files from Galaxy and splits them into a list

database_file = sys.argv[2]
#Takes the .fasta database as a .dat file 

has_xml = str(sys.argv[3])

params_file = sys.argv[4]

folder_build = sys.argv[5]
working_folder = r"C:\mq_jobs\\" + str(folder_build) + time.strftime("_%d_%m_%Y_%H_%M") + r"\\"
cmd0 = r"mkdir " + str(working_folder)
os.system(cmd0)

def without_params(file_locations, database_file, template_file, folder):
   template_base = r"""<?xml version="1.0" encoding="utf-8"?>
   <MaxQuantParams xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" aifSilWeight="4" aifIsoWeight="2" aifTopx="20" aifCorrelation="0.47" aifCorrelationFirstPass="0.8" aifMinMass="0" aifMsmsTol="10" aifSecondPass="true" aifIterative="true" aifThresholdFdr="0.01" writeMsScansTable="true" writeMsmsScansTable="true" writeMs3ScansTable="true" writeAllPeptidesTable="true" writeMzRangeTable="true">
   <name>Session1</name>
   <maxQuantVersion>1.5.2.8</maxQuantVersion>
   <tempFolder />
   <numThreads>1</numThreads>
   <sendEmail>false</sendEmail>
   <fixedCombinedFolder />
   <ionCountIntensities>false</ionCountIntensities>
   <verboseColumnHeaders>false</verboseColumnHeaders>
   <fullMinMz>-1.7976931348623157E+308</fullMinMz>
   <fullMaxMz>1.7976931348623157E+308</fullMaxMz>
   <calcPeakProperties>false</calcPeakProperties>
   <showCentroidMassDifferences>false</showCentroidMassDifferences>
   <showIsotopeMassDifferences>false</showIsotopeMassDifferences>
   <filePaths>
   </filePaths>
   <experiments>
      <string />
      <string />
   </experiments>
   <fractions>
      <short>32767</short>
      <short>32767</short>
   </fractions>
   <paramGroupIndices>
      <int>0</int>
      <int>0</int>
   </paramGroupIndices>
   <parameterGroups>
      <parameterGroup>
         <maxCharge>7</maxCharge>
         <minPeakLen>2</minPeakLen>
         <useMs1Centroids>false</useMs1Centroids>
         <useMs2Centroids>false</useMs2Centroids>
         <cutPeaks>true</cutPeaks>
         <gapScans>1</gapScans>
         <minTime>NaN</minTime>
         <maxTime>NaN</maxTime>
         <matchType>MatchFromAndTo</matchType>
         <centroidMatchTol>8</centroidMatchTol>
         <centroidMatchTolInPpm>true</centroidMatchTolInPpm>
         <centroidHalfWidth>35</centroidHalfWidth>
         <centroidHalfWidthInPpm>true</centroidHalfWidthInPpm>
         <valleyFactor>1.4</valleyFactor>
         <advancedPeakSplitting>false</advancedPeakSplitting>
         <intensityThreshold>500</intensityThreshold>
         <msInstrument>0</msInstrument>
         <intensityDetermination>0</intensityDetermination>
         <labelMods>
            <string />
         </labelMods>
         <lfqMinEdgesPerNode>3</lfqMinEdgesPerNode>
         <lfqAvEdgesPerNode>6</lfqAvEdgesPerNode>
         <fastLfq>true</fastLfq>
         <lfqMinRatioCount>2</lfqMinRatioCount>
         <useNormRatiosForHybridLfq>true</useNormRatiosForHybridLfq>
         <maxLabeledAa>0</maxLabeledAa>
         <maxNmods>5</maxNmods>
         <maxMissedCleavages>2</maxMissedCleavages>
         <multiplicity>1</multiplicity>
         <enzymes>
            <string>Trypsin/P</string>
         </enzymes>
         <enzymesFirstSearch />
         <useEnzymeFirstSearch>false</useEnzymeFirstSearch>
         <useVariableModificationsFirstSearch>false</useVariableModificationsFirstSearch>
         <variableModifications>
            <string>Acetyl (Protein N-term)</string>
            <string>Oxidation (M)</string>
         </variableModifications>
         <isobaricLabels />
         <variableModificationsFirstSearch />
         <hasAdditionalVariableModifications>false</hasAdditionalVariableModifications>
         <additionalVariableModifications />
         <additionalVariableModificationProteins />
         <doMassFiltering>true</doMassFiltering>
         <firstSearchTol>20</firstSearchTol>
         <mainSearchTol>4.5</mainSearchTol>
         <searchTolInPpm>true</searchTolInPpm>
         <isotopeMatchTol>2</isotopeMatchTol>
         <isotopeMatchTolInPpm>true</isotopeMatchTolInPpm>
         <isotopeTimeCorrelation>0.6</isotopeTimeCorrelation>
         <theorIsotopeCorrelation>0.6</theorIsotopeCorrelation>
         <recalibrationInPpm>true</recalibrationInPpm>
         <intensityDependentCalibration>false</intensityDependentCalibration>
         <minScoreForCalibration>70</minScoreForCalibration>
         <matchLibraryFile>false</matchLibraryFile>
         <libraryFile />
         <matchLibraryMassTolPpm>0</matchLibraryMassTolPpm>
         <matchLibraryTimeTolMin>0</matchLibraryTimeTolMin>
         <matchLabelTimeTolMin>0</matchLabelTimeTolMin>
         <reporterMassTolerance>NaN</reporterMassTolerance>
         <reporterPif>NaN</reporterPif>
         <filterPif>false</filterPif>
         <reporterFraction>NaN</reporterFraction>
         <reporterBasePeakRatio>NaN</reporterBasePeakRatio>
         <lcmsRunType>Standard</lcmsRunType>
         <lfqMode>0</lfqMode>
         <enzymeMode>0</enzymeMode>
         <enzymeModeFirstSearch>0</enzymeModeFirstSearch>
      </parameterGroup>
   </parameterGroups>
   <fixedModifications>
      <string>Carbamidomethyl (C)</string>
   </fixedModifications>
   <multiModificationSearch>false</multiModificationSearch>
   <compositionPrediction>false</compositionPrediction>
   <fastaFiles>
   </fastaFiles>
   <fastaFilesFirstSearch />
   <fixedSearchFolder />
   <advancedRatios>true</advancedRatios>
   <rtShift>false</rtShift>
   <separateLfq>false</separateLfq>
   <lfqStabilizeLargeRatios>true</lfqStabilizeLargeRatios>
   <lfqRequireMsms>true</lfqRequireMsms>
   <decoyMode>revert</decoyMode>
   <specialAas>KR</specialAas>
   <includeContaminants>true</includeContaminants>
   <equalIl>false</equalIl>
   <topxWindow>100</topxWindow>
   <maxPeptideMass>4600</maxPeptideMass>
   <minDeltaScoreUnmodifiedPeptides>0</minDeltaScoreUnmodifiedPeptides>
   <minDeltaScoreModifiedPeptides>6</minDeltaScoreModifiedPeptides>
   <minScoreUnmodifiedPeptides>0</minScoreUnmodifiedPeptides>
   <minScoreModifiedPeptides>40</minScoreModifiedPeptides>
   <filterAacounts>true</filterAacounts>
   <secondPeptide>true</secondPeptide>
   <matchBetweenRuns>false</matchBetweenRuns>
   <matchUnidentifiedFeatures>false</matchUnidentifiedFeatures>
   <matchBetweenRunsFdr>false</matchBetweenRunsFdr>
   <reQuantify>false</reQuantify>
   <dependentPeptides>false</dependentPeptides>
   <dependentPeptideFdr>0</dependentPeptideFdr>
   <dependentPeptideMassBin>0</dependentPeptideMassBin>
   <msmsConnection>false</msmsConnection>
   <ibaq>false</ibaq>
   <useDeltaScore>false</useDeltaScore>
   <splitProteinGroupsByTaxonomy>false</splitProteinGroupsByTaxonomy>
   <avalon>false</avalon>
   <ibaqLogFit>false</ibaqLogFit>
   <razorProteinFdr>true</razorProteinFdr>
   <deNovoSequencing>false</deNovoSequencing>
   <deNovoVarMods>true</deNovoVarMods>
   <massDifferenceSearch>false</massDifferenceSearch>
   <minPepLen>7</minPepLen>
   <peptideFdr>0.01</peptideFdr>
   <proteinFdr>0.01</proteinFdr>
   <siteFdr>0.01</siteFdr>
   <minPeptideLengthForUnspecificSearch>8</minPeptideLengthForUnspecificSearch>
   <maxPeptideLengthForUnspecificSearch>25</maxPeptideLengthForUnspecificSearch>
   <useNormRatiosForOccupancy>true</useNormRatiosForOccupancy>
   <minPeptides>1</minPeptides>
   <minRazorPeptides>1</minRazorPeptides>
   <minUniquePeptides>0</minUniquePeptides>
   <useCounterparts>false</useCounterparts>
   <advancedSiteIntensities>true</advancedSiteIntensities>
   <minRatioCount>2</minRatioCount>
   <restrictProteinQuantification>true</restrictProteinQuantification>
   <restrictMods>
      <string>Acetyl (Protein N-term)</string>
      <string>Oxidation (M)</string>
   </restrictMods>
   <matchingTimeWindow>0</matchingTimeWindow>
   <alignmentTimeWindow>0</alignmentTimeWindow>
   <numberOfCandidatesMultiplexedMsms>25</numberOfCandidatesMultiplexedMsms>
   <numberOfCandidatesMsms>15</numberOfCandidatesMsms>
   <massDifferenceMods />
   <crossLinkerSearch>false</crossLinkerSearch>
   <crossLinker />
   <msmsParamsArray>
      <msmsParams Name="FTMS" MatchToleranceInPpm="true" DeisotopeToleranceInPpm="true" DeNovoToleranceInPpm="true" Deisotope="true" Topx="12" HigherCharges="true" IncludeWater="true" IncludeAmmonia="true" DependentLosses="true" Recalibration="false">
         <MatchTolerance>20</MatchTolerance>
         <DeisotopeTolerance>7</DeisotopeTolerance>
         <DeNovoTolerance>10</DeNovoTolerance>
      </msmsParams>
      <msmsParams Name="ITMS" MatchToleranceInPpm="false" DeisotopeToleranceInPpm="false" DeNovoToleranceInPpm="false" Deisotope="false" Topx="8" HigherCharges="true" IncludeWater="true" IncludeAmmonia="true" DependentLosses="true" Recalibration="false">
         <MatchTolerance>0.5</MatchTolerance>
         <DeisotopeTolerance>0.15</DeisotopeTolerance>
         <DeNovoTolerance>0.25</DeNovoTolerance>
      </msmsParams>
      <msmsParams Name="TOF" MatchToleranceInPpm="true" DeisotopeToleranceInPpm="false" DeNovoToleranceInPpm="false" Deisotope="true" Topx="10" HigherCharges="true" IncludeWater="true" IncludeAmmonia="true" DependentLosses="true" Recalibration="false">
         <MatchTolerance>40</MatchTolerance>
         <DeisotopeTolerance>0.01</DeisotopeTolerance>
         <DeNovoTolerance>0.02</DeNovoTolerance>
      </msmsParams>
      <msmsParams Name="Unknown" MatchToleranceInPpm="false" DeisotopeToleranceInPpm="false" DeNovoToleranceInPpm="false" Deisotope="false" Topx="8" HigherCharges="true" IncludeWater="true" IncludeAmmonia="true" DependentLosses="true" Recalibration="false">
         <MatchTolerance>0.5</MatchTolerance>
         <DeisotopeTolerance>0.15</DeisotopeTolerance>
         <DeNovoTolerance>0.25</DeNovoTolerance>
      </msmsParams>
   </msmsParamsArray>
   <quantMode>1</quantMode>
   </MaxQuantParams>"""
 
   template_soup = BeautifulSoup(template_base,"xml")
   #Places the template into Beatiful Soup

   file_path_tag = template_soup.filePaths
   #Locates the tag that spcifies the raw file path in soup

   for i in file_locations: 
      new_tag = template_soup.new_tag("string")
      file_path_tag.append(new_tag)
      #Creates a new tag named <string> inside filePaths
      cmd = r"copy " + str(i) + r" " + str(folder)
      os.system(cmd)
      #Copies the dat files to mq_jobs
      new_string = i.split('\\')[-1]
      #Breaks the original file path into the file name w/ extension
      root = new_string.split(".")[0]
      #Creates root which is just the file root
      cmd1 = r"rename " +str(folder) + str(new_string) + r" " + str(root) + r".raw"
      os.system(cmd1)
      #Renames the file to .raw
      new_tag.string = str(folder) + str(root) + r".raw"
      #Adds the file path to the string tag (new_tag is named string the .string changes the path inside the string tags)
      #Entire loop does it for every .dat file specified by Galaxy

   fasta_path_tag = template_soup.fastaFiles
   #Locates the Fasta file path in templae
   new_tag = template_soup.new_tag("string")
   fasta_path_tag.append(new_tag)
   #Creates a new tag named <string> inside fastaFiles
   cmd2 = r"copy " + str(database_file) + r" " + str(folder)
   os.system(cmd2)
   #Copies the dat files to mq_jobs
   new_string = database_file.split('\\')[-1]
   #Breaks the original file path into the file name w/ extension
   root = new_string.split(".")[0]
   #Creates root which is just the file root
   cmd3 = r"rename " + str(folder) + str(new_string) + r" " + str(root) + r".fasta"
   os.system(cmd3)
   #Renames the file to .fasta
   new_tag.string = str(folder) + str(root) + r'.fasta'
   #Adds the file path to the string tag (new_tag is named string the .string changes the path inside the string tags)

   template_file.write(str(template_soup))
   cmd4 = r"copy .\mqpar.xml " + str(folder)
   os.system(cmd4)
   #Writes the newly edited template to mqpar.xml and copies it mq_jobs

   compare_soup = BeautifulSoup(open(str(folder) + r'mqpar.xml','r'),'xml')
   #Opens the copied mqpar.xml into Beutiful Soup for comparison
   if compare_soup != template_soup:
      bad_mqpar = open(str(folder) + 'mqpar.xml','w')
      bad_mqpar.write(str(template_soup))
      bad_mqpar.close()
      #Check the copied mqpar.xml file is the same as the edited template, if not rewrites it

   template_file.close()
   #Close mqpar.xml so it can be used by MaxQuant

   cmd5 = r"MaxQuantCmd.exe " + str(folder) + r"mqpar.xml"
   os.system(cmd5)
   #Runs MaxQuantCMD.ex with newly create mqpar.xml file

   cmd6 = r"copy "+ str(folder) + r"combined\txt\peptides.txt ."
   os.system(cmd6)
   #Copies the summary.txt to working directory
   os.rename("peptides.txt", str(sys.argv[6]))
   #Renames the summary.txt what is specified as the output by Galaxy


def has_params(file_locations_joined, database_file, template_file, folder):
   cmd = r"copy " + str(template_file) + r" " + str(folder)
   os.system(cmd)

   new_string = template_file.split('\\')[-1]
   root = new_string.split(".")[0]

   cmd1 = r"rename "+ str(folder) + str(new_string) + r" " + str(root) + r".xml"
   os.system(cmd1)

   template_file1 = open(str(folder) + str(root) + ".xml",'r')
   template_soup = BeautifulSoup(template_file1, 'xml')

   file_path_tag = template_soup.filePaths
   #Locates the tag that spcifies the raw file path in soup

   file_path_tag.clear()
   
   for i in file_locations: 
      new_tag = template_soup.new_tag("string")
      file_path_tag.append(new_tag)
      #Creates a new tag named <string> inside filePaths
      cmd2 = r"copy " + str(i) + r" " + str(folder)
      os.system(cmd2)
      #Copies the dat files to mq_jobs
      new_string = i.split('\\')[-1]
      #Breaks the original file path into the file name w/ extension
      root = new_string.split(".")[0]
      #Creates root which is just the file root
      cmd3 = r"rename " + str(folder) + str(new_string) + r" " + str(root) + r".raw"
      os.system(cmd3)
      #Renames the file to .raw
      new_tag.string = str(folder) + str(root) + r".raw"
      #Adds the file path to the string tag (new_tag is named string the .string changes the path inside the string tags)
      #Entire loop does it for every .dat file specified by Galaxy

   fasta_path_tag = template_soup.fastaFiles
   #Locates the Fasta file path in template
   fasta_path_tag.clear()
   new_tag = template_soup.new_tag("string")
   fasta_path_tag.append(new_tag)
   #Creates a new tag named <string> inside fastaFiles
   cmd4 = r"copy " + str(database_file) + r" " + str(folder)
   os.system(cmd4)
   #Copies the dat files to mq_jobs
   new_string = database_file.split('\\')[-1]
   #Breaks the original file path into the file name w/ extension
   root = new_string.split(".")[0]
   #Creates root which is just the file root
   cmd5 = r"rename " + str(folder) + str(new_string) + r" " + str(root) + r".fasta"
   os.system(cmd5)
   #Renames the file to .fasta
   new_tag.string = str(folder) + str(root) + r'.fasta'
   #Adds the file path to the string tag new_tag is named string the .string changes 

   template_file1.close()

   template_file2 = open(str(folder) + r"mqpar.xml",'w')
   template_file2.write(str(template_soup))

   template_file2.close()
   #Close mqpar.xml so it can be used by MaxQuant

   cmd6 = r"MaxQuantCmd.exe " + str(folder) + "mqpar.xml"
   os.system(cmd6)
   #Runs MaxQuantCMD.exe with newly create mqpar.xml file

   cmd7 = r"copy " + str(folder) + r"combined\txt\peptides.txt ."
   os.system(cmd7)

   os.rename("peptides.txt", str(sys.argv[6]))
   #Renames the summary.txt what is specified as the output by Galaxy


if (has_xml == "true"):
   has_params(file_locations, database_file, params_file, working_folder)
elif (has_xml == "false"):
   template_file = open('mqpar.xml','w')
   #Creates mqpar.xml file
   without_params(file_locations, database_file, template_file, working_folder)
