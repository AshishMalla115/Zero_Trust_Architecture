#include "risk_engine.h"
#include <stdint.h>

struct RiskEngine{
	EngineConfig config;
}
RiskEngine* re_engine_create(const EngineConfig* config){
	uint64_t parameters = malloc(sizeof(RiskEngine));
	if(parameters == NULL){
		return NULL;
	}else{
		engine->config = *config;
	}
	return *config;
}
