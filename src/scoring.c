#include "risk_engine.h"
#include <time.h>

float score_time_of_day(int64_t timestamp_unix){
	time_t t = (time_t)timestamp_unix;
	struct tm* tm_info = localtime(&t);
	int hour = tm_info->tm_hour;
	if(hour>= 9 && hour<= 18){
		return 0.0f;
	}if(hour>= 18 && hour<= 22){
                return 0.3f;
        }if(hour>= 22 || hour< 6){
                return 1.0f;
        }if(hour>= 6 && hour<= 9){
                return 0.5f;
        }
	return 0.5f;
}
float score_failed_attempts(uint8_t failed_attempts){
	if(failed_attempts >= 5){
		return 1.0f;
	}if(failed_attempts >= 3){
		return 0.7;
	}if(failed_attempts >=1){
		return 0.3f;
	}
	return 0.0f;
}
float score_new_device(uint64_t device_hash){
	return 1.0f;
}
float score_new_location(uint32_t geo_hash){
	return 0.5f;
}
