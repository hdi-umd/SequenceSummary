library(lme4)
library(sjstats)

library(haven) # to load the SPSS .sav file
library(tidyverse) # needed for data manipulation.
library(RColorBrewer) # needed for some extra colours in one of the graphs
library(lmerTest)# to get p-value estimations that are not part of the standard lme4 packages
#Load Data
data1 <- read.csv(file = "./Documents/Research/code/Analysis/survey_data.csv", header=TRUE,  stringsAsFactors=TRUE)
data1

# Convert to factor
data1$Dataset<- factor(data1$Dataset)
data1$Task<- factor(data1$Task)
data1$Insight<- factor(data1$Insight)
data1$Method<- factor(data1$Method)
data1$LikertScore<- factor(data1$LikertValue)

#Convert to int
data1$Dataset<-  as.integer(data1$Dataset)
data1$Task<- as.integer(data1$Task)
data1$Insight<- as.integer(data1$Insight)
data1$Method<- as.integer(data1$Method)
data1$LikertScore<- as.integer(data1$LikertScore)

## Random Intercept Model
#Level 0 Model
modelLinear <- lm(LikertScore ~ 1, data = data1)
summary(modelLinear)

#Level 1 Model- Record
model2LinearRecord <- lmer(LikertScore ~  1 + (1|Record), REML = FALSE, data = data1)
summary(model2LinearRecord)
performance::icc(model2LinearRecord)
anova(model2LinearRecord, modelLinear)

#Level 1 Model- Task
model2LinearTask <- lmer(LikertScore ~ 1+(1|Task), REML = FALSE, data = data1)
summary(model2LinearTask)
performance::icc(model2LinearTask)
anova(model2LinearTask, modelLinear)

#Level 1 Model- Dataset
model2LinearDataset <- lmer(LikertScore ~ 1+(1|Dataset), REML = FALSE, data = data1)
summary(model2LinearDataset)
performance::icc(model2LinearDataset)
anova(model2LinearDataset, modelLinear)

#Level 1 Model- Insight
model2LinearInsight <- lmer(LikertScore ~ 1+(1|Insight), REML = FALSE, data = data1)
summary(model2LinearInsight)
performance::icc(model2LinearInsight)
anova(model2LinearInsight, modelLinear)


#Level 1 Model-MSP
model2LinearMSP <- lmer(LikertScore ~ 1+(1|MSP), REML = FALSE, data = data1)
summary(model2LinearMSP)
performance::icc(model2LinearMSP)
anova(model2LinearMSP, modelLinear)


#Level 1 Model-Method
model2LinearMethod <- lmer(LikertScore ~ 1+(1|Method), REML = FALSE, data = data1)
summary(model2LinearMethod)
performance::icc(model2LinearMethod)
anova(model2LinearMethod, modelLinear)

#Level2 Model-Record
model3LinearRecord <- lmer(LikertScore ~ 1+(1|Record/Dataset), REML = FALSE, data = data1)
summary(model3LinearRecord)
performance::icc(model3LinearRecord)
anova(model3LinearRecord, modelLinear)

#Level2 Model-Method
model3LinearRecord <- lmer(LikertScore ~ 1+(1|Record/Dataset), REML = FALSE, data = data1)
summary(model3LinearRecord)
performance::icc(model3LinearRecord)
anova(modelLinear, model3LinearRecord)

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

modelMixed2 <- lmer(LikertScore ~ Insight * Method +(1|Task/Dataset/Record) + +(1|MSP/Record), REML = FALSE, data = data1)
summary(modelMixed2)
performance::icc(modelMixed2)
anova(modelMixed2, modelLinear)


### Mixed Effect Model-3
#### Assumptions- Fixed Effect- Insight Method
#### Assumptions- Random Effect- Record, Dataset, Task, MSP

modelMixed3 <- lmer(LikertScore ~ Insight + Method +(1|Task/Dataset/Record) + +(1|MSP/Record), REML = FALSE, data = data1)
summary(modelMixed3)
performance::icc(modelMixed3)
anova(modelMixed3, modelLinear)

### Mixed Effect Model-3
#### Assumptions- Fixed Effect- Method
#### Assumptions- Random Effect- Record, Dataset, Task, MSP

modelMixed3 <- lmer(LikertScore ~ Method +(1|Task/Dataset/Record) + +(1|MSP/Record), REML = FALSE, data = data1)
summary(modelMixed3)
performance::icc(modelMixed3)
anova(modelMixed3, modelLinear)

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

