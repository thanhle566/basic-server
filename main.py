from fastapi import FastAPI
from dynatraceController import router as dynatrace_router
from opensearchController import router as opensearch_router
from grafanaController import router as grafana_router
from influxController import router as influx_router

app = FastAPI()

app.include_router(dynatrace_router)
app.include_router(opensearch_router)
app.include_router(grafana_router)
app.include_router(influx_router)