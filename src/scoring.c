#include "risk_engine.h"
#include <time.h>

float score_time_of_day(int64_t timestamp_unix){
	time_t t = (time_t)timestamp_unix;
	struct tm* tm_info = localtime(&t);
	int hour = tm_info->tm_hour;
	if(hour>= 9 && hour<= 18){
		return 0.0;
	}if(hour>= 18 && hour<= 22){
                return 0.3;
        }if(hour>= 22 && hour<= 6){
                return 1.0;
        }if(hour>= 6 && hour<= 9){
                return 0.5;
        }
	return 0.5f;
}

