{{/*
Expand the name of the chart.
*/}}
{{- define "clusterAutoscaler.name" }}
{{- default (printf "%s-%s" .Values.clusterAutoscaler.cloudProvider .Chart.Name) .Values.clusterAutoscaler.nameOverride | trunc 63 | trimSuffix "-" -}}
{{- end }}


{/*
Create a default fully qualified app name.
We truncate at 63 chars because some Kubernetes name fields are limited to this (by the DNS naming spec).
*/}}
{{- define "clusterAutoscaler.fullname" -}}
{{- if .Values.clusterAutoscaler.fullnameOverride -}}
{{- .Values.clusterAutoscaler.fullnameOverride | trunc 63 | trimSuffix "-" -}}
{{- else -}}
{{- $name := default (printf "%s-%s" .Values.clusterAutoscaler.cloudProvider .Chart.Name) .Values.nameOverride -}}
{{- if ne $name .Release.Name -}}
{{- printf "%s-%s" .Release.Name $name | trunc 63 | trimSuffix "-" -}}
{{- else -}}
{{- printf "%s" $name | trunc 63 | trimSuffix "-" -}}
{{- end -}}
{{- end -}}
{{- end -}}

{{/*
Common labels
*/}}
{{- define "clusterAutoscaler.labels" -}}
{{- include "clusterAutoscaler.selectorLabels" . }}
{{- end }}


{{/*
Selector labels
*/}}
{{- define "clusterAutoscaler.selectorLabels" }}
{{- if .Values.clusterAutoscaler.labels -}}
{{- range $key, $val := .Values.clusterAutoscaler.labels -}}
{{ $key }}: {{ $val | quote }}
{{- end }}
{{- end }}
{{- end }}
