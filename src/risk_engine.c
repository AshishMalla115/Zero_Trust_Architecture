#include "risk_engine.h"
#include <stdlib.h>

struct RiskEngine{
	EngineConfig config;
};
RiskEngine* re_engine_create(const EngineConfig* config){
	RiskEngine* engine = malloc(sizeof(RiskEngine));
	if(engine == NULL){
		return NULL;
	}
	engine->config = *config;
	return engine;
}
void  re_engine_destroy(RiskEngine* engine){
	free(engine);
}
