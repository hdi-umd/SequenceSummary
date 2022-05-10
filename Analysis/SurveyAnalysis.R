library(lme4)
library(sjstats)
library(MuMIn)
library(haven) # to load the SPSS .sav file
library(tidyverse) # needed for data manipulation.
library(RColorBrewer) # needed for some extra colours in one of the graphs
library(lmerTest)# to get p-value estimations that are not part of the standard lme4 packages
library(specr)
library(ordinal)
#Load Data
data1 <- read.csv(file = "./Documents/Research/code/Analysis/survey_data.csv", header=TRUE,  stringsAsFactors=TRUE)
data1

# Convert to factor
data1$Dataset<- factor(data1$Dataset)
data1$Task<- factor(data1$Task)
data1$Insight<- factor(data1$Insight)
data1$Method<- factor(data1$Method)
data1$LikertScore<- factor(data1$LikertValue)
data1$LikertScaleF = as.factor(data1$LikertScale)
#Convert to int
data1$Dataset<-  as.integer(data1$Dataset)
data1$Task<- as.integer(data1$Task)
data1$Insight<- as.integer(data1$Insight)
data1$Method<- as.integer(data1$Method)
data1$LikertScore<- as.integer(data1$LikertScore)

## Random Intercept Model
#Level 0 Model
modelLinear <- lm(LikertScale ~ 1, data = data1)
summary(modelLinear)

#Level 1 Model- Record
model2LinearRecord <- lmer(LikertScale ~  1 + (1|Record), REML = FALSE, data = data1)
summary(model2LinearRecord)
performance::icc(model2LinearRecord)
anova(model2LinearRecord, modelLinear)
icc_specs(model2LinearRecord) %>%
  mutate_if(is.numeric, round, 2)


#Level 1 Model- Task
model2LinearTask <- lmer(LikertScale ~ 1+(1|Task), REML = FALSE, data = data1)
summary(model2LinearTask)
performance::icc(model2LinearTask)
anova(model2LinearTask, modelLinear)
icc_specs(model2LinearTask) %>%
  mutate_if(is.numeric, round, 2)

#Level 1 Model- Dataset
model2LinearDataset <- lmer(LikertScale ~ 1+(1|Dataset), REML = FALSE, data = data1)
summary(model2LinearDataset)
performance::icc(model2LinearDataset)
anova(model2LinearDataset, modelLinear)
icc_specs(model2LinearDataset) %>%
  mutate_if(is.numeric, round, 2)


#Level 1 Model- Insight
model2LinearInsight <- lmer(LikertScale ~ 1+(1|Insight), REML = FALSE, data = data1)
summary(model2LinearInsight)
performance::icc(model2LinearInsight)
anova(model2LinearInsight, modelLinear)
icc_specs(model2LinearInsight) %>%
  mutate_if(is.numeric, round, 2)


#Level 1 Model-MSP
model2LinearMSP <- lmer(LikertScale ~ 1+(1|MSP), REML = FALSE, data = data1)
summary(model2LinearMSP)
performance::icc(model2LinearMSP)
anova(model2LinearMSP, modelLinear)
icc_specs(model2LinearMSP) %>%
  mutate_if(is.numeric, round, 2)


#Level 1 Model-Method
model2LinearMethod <- lmer(LikertScale ~ 1+(1|Method), REML = FALSE, data = data1)
summary(model2LinearMethod)
performance::icc(model2LinearMethod)
anova(model2LinearMethod, modelLinear)
icc_specs(model2LinearMethod) %>%
  mutate_if(is.numeric, round, 2)

#Level 1 ALL
model2Linear <- lmer(LikertScale ~ 1+(1|Record)++(1|Dataset)+(1|Insight)+(1|Task)+(1|MSP), REML = FALSE, data = data1)
summary(model2Linear)
performance::icc(model2Linear)
anova(model2Linear, modelLinear)
icc_specs(model2Linear) %>%
  mutate_if(is.numeric, round, 2)



#Level2 Model-Record Dataset
model3LinearRecordDataset <- lmer(LikertScale ~ 1+(1|Dataset/Record), REML = FALSE, data = data1)
summary(model3LinearRecordDataset)
performance::icc(model3LinearRecordDataset)
anova(model3LinearRecordDataset, model2LinearRecord)
icc_specs(model3LinearRecordDataset) %>%
  mutate_if(is.numeric, round, 2)


#Level2 Model-Record Task
model3LinearRecordTask <- lmer(LikertScale ~ 1+(1|Task/Record), REML = FALSE, data = data1)
summary(model3LinearRecordTask)
performance::icc(model3LinearRecordTask)
anova(model3LinearRecordTask, modelLinear)
anova(model3LinearRecordTask, model2LinearRecord)
icc_specs(model3LinearRecordTask) %>%
  mutate_if(is.numeric, round, 2)

#Level2 Model-Record MSP
model3LinearRecordMSP <- lmer(LikertScale ~ 1+(1|MSP/Record), REML = FALSE, data = data1)
summary(model3LinearRecordMSP)
performance::icc(model3LinearRecordMSP)
anova( model3LinearRecordMSP, modelLinear)
anova(model3LinearRecordMSP, model2LinearRecord)
icc_specs(model3LinearRecordMSP) %>%
  mutate_if(is.numeric, round, 2)

#Level2 Model-Record Insight
model3LinearRecordInsight <- lmer(LikertScale ~ 1+(1|Record/Insight), REML = FALSE, data = data1)
summary(model3LinearRecordInsight)
performance::icc(model3LinearRecordInsight)
anova( model3LinearRecordInsight, modelLinear)
anova(model3LinearRecordInsight, model2LinearRecord)
icc_specs(model3LinearRecordInsight) %>%
  mutate_if(is.numeric, round, 2)

#Level2 Model-Record Insight Crossed
model3LinearRecordInsightCrossed <- lmer(LikertScale ~ 1+(1|Record) + (1|Insight), REML = FALSE, data = data1)
summary(model3LinearRecordInsightCrossed)
performance::icc(model3LinearRecordInsightCrossed)
anova( model3LinearRecordInsightCrossed, modelLinear)
anova(model3LinearRecordInsightCrossed, model2LinearRecord)
icc_specs(model2Linear) %>%
  mutate_if(is.numeric, round, 2)

#Level2 Model-Record Insight Crossed Interaction
model3LinearRecordInsightInteraction <- lmer(LikertScale ~ 1+(1|Record) * (1|Insight), REML = FALSE, data = data1)
summary(model3LinearRecordInsightInteraction)
performance::icc(model3LinearRecordInsightInteraction)
anova( model3LinearRecordInsightInteraction, modelLinear)
anova(model3LinearRecordInsightInteraction, model2LinearRecord)
anova(model3LinearRecordInsightInteraction)
icc_specs(model2Linear) %>%
  mutate_if(is.numeric, round, 2)


#Level2 Model-Task Dataset
model3LinearDatasetTask <- lmer(LikertScale ~ 1+(1|Task/Dataset), REML = FALSE, data = data1)
summary(model3LinearDatasetTask)
performance::icc(model3LinearDatasetTask)
anova(model3LinearDatasetTask, modelLinear)
anova(model3LinearDatasetTask, model2LinearRecord)
icc_specs(model3LinearDatasetTask) %>%
  mutate_if(is.numeric, round, 2)



#Level2 Model-Dataset MSP
model3LinearMSPDataset <- lmer(LikertScale ~ 1+(1|Dataset/MSP), REML = FALSE, data = data1)
summary(model3LinearMSPDataset)
performance::icc(model3LinearMSPDataset)
anova( model3LinearMSPDataset, modelLinear)
anova(model3LinearMSPDataset, model2LinearRecord)
icc_specs(model2Linear) %>%
  mutate_if(is.numeric, round, 2)

#Level2 Model-Task MSP
model3LinearMSPTask <- lmer(LikertScale ~ 1+(1|Task/MSP), REML = FALSE, data = data1)
summary(model3LinearMSPTask)
performance::icc(model3LinearMSPTask)
anova( model3LinearMSPTask, modelLinear)
anova(model3LinearMSPTask, model2LinearRecord)
icc_specs(model2Linear) %>%
  mutate_if(is.numeric, round, 2)

#Level2 Model- MSP Insight
model3LinearMSPInsight <- lmer(LikertScale ~ 1+(1|MSP/Insight), REML = FALSE, data = data1)
summary(model3LinearMSPInsight)
performance::icc(model3LinearMSPInsight)
anova( model3LinearMSPInsight, modelLinear)
anova(model3LinearMSPInsight, model2LinearInsight)
icc_specs(model2Linear) %>%
  mutate_if(is.numeric, round, 2)

anova(model3LinearRecordTask, model3LinearRecordDataset)
anova(model3LinearRecordTask, model3LinearRecordMSP)
anova(model3LinearRecordMSP, model3LinearRecordDataset)
anova(model3LinearRecordInsight, model3LinearRecordMSP)

#Level3 Model-Dataset Record Insight
model4LinearDatasetRecordInsight <- lmer(LikertScale ~ 1+(1|Dataset/Record/Insight), REML = FALSE, data = data1)
summary(model4LinearDatasetRecordInsight)
performance::icc(model4LinearDatasetRecordInsight)
anova( model4LinearDatasetRecordInsight, modelLinear)
anova(model4LinearDatasetRecordInsight, model2LinearRecord)
anova(model4LinearDatasetRecordInsight, model3LinearRecordDataset)
anova(model4LinearDatasetRecordInsight, model3LinearRecordInsight)
icc_specs(model4LinearDatasetRecordInsight) %>%
  mutate_if(is.numeric, round, 2)


#Level3 Model-Dataset Record and Insight
model4LinearDatasetRecordandInsight <- lmer(LikertScale ~ 1+(1|Dataset/Record) + (1|Record/Insight), REML = FALSE, data = data1)
summary(model4LinearDatasetRecordandInsight)
performance::icc(model4LinearDatasetRecordandInsight)
anova( model4LinearDatasetRecordandInsight, modelLinear)
anova(model4LinearDatasetRecordandInsight, model2LinearRecord)
anova(model4LinearDatasetRecordandInsight, model3LinearRecordDataset)
anova(model4LinearDatasetRecordandInsight, model3LinearRecordInsight)
icc_specs(model4LinearDatasetRecordandInsight) %>%
  mutate_if(is.numeric, round, 2)

#Level3 Model-Task Dataset Record 
model4LinearTaskDatasetRecord <- lmer(LikertScale ~ 1+(1|Task/Dataset/Record), REML = FALSE, data = data1)
summary(model4LinearTaskDatasetRecord)
performance::icc(model4LinearTaskDatasetRecord)
anova( model4LinearTaskDatasetRecord, modelLinear)
anova(model4LinearTaskDatasetRecord, model2LinearRecord)
anova(model4LinearTaskDatasetRecord, model3LinearDatasetTask)
anova(model4LinearTaskDatasetRecord, model3LinearRecordDataset)
icc_specs(model4LinearTaskDatasetRecord) %>%
  mutate_if(is.numeric, round, 2)

#Level3 Model-Task Record Insight
model4LinearTaskRecordInsight <- lmer(LikertScale ~ 1+(1|Task/Record/Insight), REML = FALSE, data = data1)
summary(model4LinearTaskRecordInsight)
performance::icc(model4LinearTaskRecordInsight)
anova( model4LinearTaskRecordInsight, modelLinear)
anova(model4LinearTaskRecordInsight, model2LinearRecord)
anova(model4LinearTaskRecordInsight, model3LinearRecordTask)
anova(model4LinearTaskRecordInsight, model3LinearRecordInsight)
icc_specs(model4LinearTaskRecordInsight) %>%
  mutate_if(is.numeric, round, 2)

#Level3 Model-Dataset MSP Record 
model4LinearDatasetMSPRecord <- lmer(LikertScale ~ 1+(1|Dataset/MSP/Record), REML = FALSE, data = data1)
summary(model4LinearDatasetMSPRecord)
performance::icc(model4LinearDatasetMSPRecord)
anova( model4LinearDatasetMSPRecord, modelLinear)
anova(model4LinearDatasetMSPRecord, model2LinearRecord)
anova(model4LinearDatasetMSPRecord, model3LinearRecordDataset)
anova(model4LinearDatasetMSPRecord, model3LinearRecordMSP)
icc_specs(model4LinearDatasetMSPRecord) %>%
  mutate_if(is.numeric, round, 2)

#Level3 Model-MSP Record Insight
model4LinearMSPRecordInsight <- lmer(LikertScale ~ 1+(1|MSP/Record/Insight), REML = FALSE, data = data1)
summary(model4LinearMSPRecordInsight)
performance::icc(model4LinearMSPRecordInsight)
anova( model4LinearMSPRecordInsight, modelLinear)
anova(model4LinearMSPRecordInsight, model2LinearRecord)
anova(model4LinearMSPRecordInsight, model3LinearRecordMSP)
anova(model4LinearMSPRecordInsight, model3LinearMSPInsight)
icc_specs(model2Linear) %>%
  mutate_if(is.numeric, round, 2)

#Level4 Model- Task Dataset Record Insight  and   
model5LinearTaskDatasetRecordInsight <- lmer(LikertScale ~ 1+(1|Task/Dataset/Record/Insight), REML = FALSE, data = data1)
summary(model5LinearTaskDatasetRecordInsight)
performance::icc(model5LinearTaskDatasetRecordInsight)
anova( model5LinearTaskDatasetRecordInsight, modelLinear)
anova(model5LinearTaskDatasetRecordInsight, model2LinearRecord)
anova(model5LinearTaskDatasetRecordInsight, model3LinearRecordDataset)
anova(model5LinearTaskDatasetRecordInsight, model3LinearRecordInsight)
anova(model5LinearTaskDatasetRecordInsight, model4LinearDatasetRecordInsight)
anova(model5LinearTaskDatasetRecordInsight, model4LinearTaskDatasetRecord)
icc_specs(model5LinearTaskDatasetRecordInsight) %>%
  mutate_if(is.numeric, round, 2)


#Level4 Model- Task Dataset Record Insight  and   MSP
model5LinearTaskDatasetRecordInsightMSP <- lmer(LikertScale ~ 1+(1|Task/MSP) + (1|Dataset/Record/Insight) , REML = FALSE, data = data1)
summary(model5LinearTaskDatasetRecordInsightMSP)
performance::icc(model5LinearTaskDatasetRecordInsightMSP)
anova( model5LinearTaskDatasetRecordInsightMSP, modelLinear)
anova(model5LinearTaskDatasetRecordInsightMSP, model2LinearRecord)
anova(model5LinearTaskDatasetRecordInsightMSP, model3LinearRecordDataset)
anova(model5LinearTaskDatasetRecordInsightMSP, model3LinearRecordInsight)
anova(model5LinearTaskDatasetRecordInsightMSP, model4LinearDatasetRecordInsight)
anova(model5LinearTaskDatasetRecordInsightMSP, model4LinearTaskDatasetRecord)
anova(model5LinearTaskDatasetRecordInsightMSP, model5LinearTaskDatasetRecordInsight)
icc_specs(model5LinearTaskDatasetRecordInsightMSP) %>%
  mutate_if(is.numeric, round, 2)

#Level4 Model- Task Dataset Record Insight  and   MSP


# MixedEffectModel
MixedEffectDatasetRecord <- lmer(LikertScale ~ 1 + Method +(1|Dataset/Record) ,  REML = FALSE, data = data1)
summary(MixedEffectDatasetRecord)
anova(MixedEffectDatasetRecord, model3LinearRecordDataset)
icc_specs(MixedEffectDatasetRecord) %>%
  mutate_if(is.numeric, round, 2)
confint(MixedEffectDatasetRecord)

#MixedEffectModel
MixedEffect2 <- lmer(LikertScale ~ 1+ Method + (1|Task/MSP) + (1|Dataset/Record/Insight) , REML = FALSE, data = data1)
summary(MixedEffect2)
anova(MixedEffect2, model5LinearTaskDatasetRecordInsightMSP)
icc_specs(MixedEffect2) %>%
  mutate_if(is.numeric, round, 2)
confint(MixedEffect2)


MixedEffect3 <- lmer(LikertScale ~ 1+ Method  + (1|Dataset/Record/Insight) , REML = FALSE, data = data1)
summary(MixedEffect3)
anova(MixedEffect3, model5LinearTaskDatasetRecordInsightMSP)
icc_specs(MixedEffect3) %>%
  mutate_if(is.numeric, round, 2)
confint(MixedEffect3)



MixedEffect3 <- glmer(LikertScale ~ 1+ Method  + (1|Dataset/Record/Insight) , data = data1)
summary(MixedEffect3)
anova(MixedEffect3, model5LinearTaskDatasetRecordInsightMSP)
icc_specs(MixedEffect3) %>%
  mutate_if(is.numeric, round, 2)
confint(MixedEffect3)
icc_specs(model2Linear) %>%
  mutate_if(is.numeric, round, 2)

MixedEffect4 <- clmm(LikertScaleF ~ 1+ Method  + (1|Dataset:Record) , data = data1, link = "probit", threshold = "equidistant")

summary(MixedEffect4)
anova(MixedEffect4, model5LinearTaskDatasetRecordInsightMSP)
icc_specs(MixedEffect4) %>%
  mutate_if(is.numeric, round, 2)








###------------####################
#Level2 Model-Record
model3LinearRecord <- lmer(LikertScore ~ 1+(1|Record/Dataset), REML = FALSE, data = data1)
summary(model3LinearRecord)
performance::icc(model3LinearRecord)
anova(model3LinearRecord, modelLinear)

#Level2 Model-Record
model3LinearRecord <- lmer(LikertScore ~ 1+(1|Record/Dataset), REML = FALSE, data = data1)
summary(model3LinearRecord)
performance::icc(model3LinearRecord)
anova(model3LinearRecord, modelLinear)




### Mixed Effect Model-1
#### Assumptions- Fixed Effect- Insight Method
#### Assumptions- Random Effect- Record, Dataset, Task, MSP

modelMixed1 <- lmer(LikertScore ~ Insight * Method +(1|Task/Dataset/MSP/Record), REML = FALSE, data = data1)
summary(modelMixed1)
performance::icc(modelMixed1)
anova(modelMixed1, modelLinear)


### Mixed Effect Model-2
#### Assumptions- Fixed Effect- Insight Method
#### Assumptions- Random Effect- Record, Dataset, Task, MSP

modelMixed2 <- lmer(LikertScore ~ Insight * Method +(1|Task/Dataset/Record) + (1|MSP/Record), REML = FALSE, data = data1)
summary(modelMixed2)
performance::icc(modelMixed2)
anova(modelMixed2, modelLinear)


### Mixed Effect Model-3
#### Assumptions- Fixed Effect- Insight Method
#### Assumptions- Random Effect- Record, Dataset, Task, MSP

modelMixed3 <- lmer(LikertScore ~ Insight + Method +(1|Task/Dataset/Record) + (1|MSP/Record), REML = FALSE, data = data1)
summary(modelMixed3)
performance::icc(modelMixed3)
anova(modelMixed3, modelLinear)

### Mixed Effect Model-4
#### Assumptions- Fixed Effect- Method
#### Assumptions- Random Effect- Record, Dataset, Task, MSP

modelMixed4 <- lmer(LikertScore ~ Method*Insight +(1|Task/Dataset/Record), REML = FALSE, data = data1)
summary(modelMixed4)
performance::icc(modelMixed4)
anova(modelMixed4, modelLinear)

### Mixed Effect Model-5
#### Assumptions- Fixed Effect- Method, Insight
#### Assumptions- Random Effect- Record, Dataset, Task, 

modelMixed5 <- lmer(LikertScore ~ Method +(1|Task/Dataset/Record) , REML = FALSE, data = data1)
summary(modelMixed5)
performance::icc(modelMixed5)
anova(modelMixed5, modelLinear)

data1$Liker
MixedModel6<- clmm(LikertScore ~ Method +(1|Task/Dataset/Record),data = data1, link = "probit", threshold = "equidistant")

##########################################
#Level 1 Model- Method
model2Linear <- lmer(LikertScore ~ (1|Record), REML = FALSE, data = data1)
summary(model2Linear)
performance::icc(model2LinearTask)
anova(model2LinearRecord, modelLinear)

model1 <- lm(LikertScore ~ Method + Task + Insight + MSP, data = data1)
summary(model1)

model2 <- lm(LikertScore ~ Method + Dataset + Insight + MSP, data = data1)
summary(model2)

