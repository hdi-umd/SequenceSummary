#!/bin/bash

#emergency department
python RunAll.py --file "datasets/emergency_department/AAAsample_ed2.txt" --evttype 1 --startidx 2 --format "%Y-%m-%d %H:%M:%S" --sep "\t" --local True --header "record_id" "event_category" "Start_time" "end_time" "event_attributes" --grpattr "record_id" --attr "event_category"

python RunAll.py --file "datasets/emergency_department/study_died.txt" --evttype 1 --startidx 2 --format "%Y-%m-%d %H:%M:%S.%f" --sep "\t" --local True --header "record_id" "event_category" "Start_time" "end_time" "event_attributes" --grpattr "record_id" --attr "event_category"

python RunAll.py --file "datasets/emergency_department/study_lived.txt" --evttype 1 --startidx 2 --format "%Y-%m-%d %H:%M:%S.%f" --sep "\t" --local True --header "record_id" "event_category" "Start_time" "end_time" "event_attributes" --grpattr "record_id" --attr "event_category"

#Chicago Bulls
python RunAll.py --file "datasets/Chicago_Bulls/CHICAGO-SeasonD2O.txt" --evttype 3 --startidx 2 --endidx 3 --format "%H:%M:%S.%f" --sep "\t" --local True --header "record_id" "event_category" "Start_time" "end_time" "event_attributes" --grpattr "record_id" --attr "event_category"

python RunAll.py --file "datasets/Chicago_Bulls/CHICAGO-SeasonO2D.txt" --evttype 3 --startidx 2 --endidx 3 --format "%H:%M:%S.%f" --sep "\t" --local True --header "record_id" "event_category" "Start_time" "end_time" "event_attributes" --grpattr "record_id" --attr "event_category"

#Sequence Braiding
python RunAll.py --file "datasets/sequence_braiding/sequence_braiding_refined.csv" --evttype 1 --startidx 0 --format "%m/%d/%y" --sep "," --local True --split "week" --attr "Meal"

#Children Hospital
python RunAll.py --file "datasets/Children_Hospital/DND-ChildrensDemo-06-26-13.txt" --evttype 3 --startidx 2 --endidx 3  --format "%Y-%m-%d %H:%M:%S.%f" --sep "\t" --local True --header "record_id" "event_category" "Start_time" "end_time" "event_attributes" --grpattr "record_id" --attr "event_category"

#Coreflow Paper Test
python RunAll.py --file "datasets/coreflow_sample/corelow_paper_test.csv" --evttype 1 --startidx 1 --format "%m/%d/%y" --sep "," --local True --grpattr "Category" --attr "Event"

#Highway incidents
python RunAll.py --file "datasets/highway_incidents/high_event.txt" --evttype 1 --startidx 2 --format "%Y-%m-%d %H:%M:%S-%z:%Z" --sep "\t" --local True  --header "record_id" "event_category" "Start_time" "end_time" "event_attributes" --grpattr "record_id" --attr "event_category"

#Invention Trajectories
python RunAll.py --file "datasets/Invention_Trajectories/illinois03.txt" --evttype 3 --startidx 2 --endidx 3 --format "%m/%d/%Y" --sep "\t" --local True  --header "record_id" "event_category" "Start_time" "end_time" "event_attributes" --grpattr "record_id" --attr "event_category"

#Foursquare Tokyo
python RunAll.py --file "datasets/foursquare/tokyo.txt" --evttype 1 --startidx 7 --format "%a %b %d %H:%M:%S %z %Y" --sep "\t" --local True  --header "User_ID" "Venue_ID" "Venue_category_ID" "Venue_category_name" "Latitude" "Longitude" "Timezone offset" "UTC Time" --grpattr "User_ID" --attr "Venue_category_name"

#Foursquare NYC