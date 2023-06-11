{{/*
Expand the name of the chart.
*/}}
{{- define "app.name" -}}
{{- default .Chart.Name .Values.flaskApp.nameOverride | trunc 63 | trimSuffix "-" -}}
{{- end -}}
