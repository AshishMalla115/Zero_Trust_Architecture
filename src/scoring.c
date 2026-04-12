#include "risk_engine.h"
#include <time.h>

time_t t = (time_t)timestamp_unix; 
struct tm* tm_info = localtime(&t); 
int hour = tm_info->tm_hour;

float score_time_of_day(int64_t timestamp_unix){
	if(timestamp_unix >= 9 && timestamp_unix <= 18){
		return 0.0;
	}if(timestamp_unix >= 18 && timestamp_unix <= 22){
                return 0.3;
        }if(timestamp_unix >= 22 && timestamp_unix <= 6){
                return 1.0;
        }if(timestamp_unix >= 6 && timestamp_unix <= 9){
                return 0.5;
        }
}

