---
title: "Tracing API Reference"
description: "REST endpoints for GGX tracing: OTLP ingest, traces, spans, sessions, scores, score configs, masking, evaluators, monitors, exports, saved views and findings."
---

All endpoints take your API key in the `x-api-key` header. Request and response fields use camelCase.

## Traces, spans and sessions

| Endpoint | What it does |
| --- | --- |
| `POST /api/v1/traces/otlp` | Send OpenTelemetry spans. See [Sending traces](../sending-traces/#with-any-opentelemetry-exporter). |
| `GET /api/v1/traces` | List traces. Filters include `startTime`/`endTime`, `projectId`, `environment`, `status`, `sessionId`, `userId`, `search`, `scoreName` with `scoreMin`/`scoreMax`/`scoreLabel`, `flag` (`duplicate_tools`, `loop`, `cost_outlier`, `empty_output`; repeatable), `query` (the [query language](../search-and-analytics/#the-query-box)), `dim` (`key:value`) and `platform`. |
| `GET /api/v1/traces/summary` | Counts, error rate, latency percentiles (p50, p90, p95, p99), cost, and masked and flagged span counts for a filter. |
| `GET /api/v1/traces/{traceId}` | One trace with its span tree. |
| `GET /api/v1/traces/{traceId}/spans/{spanId}` | One span in full, with its events, time to first token and data-quality flags. |
| `GET /api/v1/traces/sessions` | Sessions for a filter (`flagged=true` for flagged sessions only); `/sessions/{sessionId}` for one. |
| `GET /api/v1/traces/spans` | Search spans across traces; `GET /traces/query-fields` lists the query fields. |
| `GET /api/v1/traces/timeseries` | Any monitor measure per time bucket, optionally grouped by a field or dimension. |
| `GET /api/v1/traces/export`, `/traces/spans/export` | Export as CSV or JSON Lines; `GET /traces/exports` lists the export record. |

## Scores

| Endpoint | What it does |
| --- | --- |
| `POST /api/v1/trace-scores` | Add or update 1 to 100 scores, all or nothing. |
| `GET /api/v1/trace-scores` | A trace's scores (`?traceId=`) or a session's (`?sessionId=`). |
| `PATCH` / `DELETE /api/v1/trace-scores/{id}` | Change or remove one of your scores. |
| `GET /api/v1/trace-scores/summary` | Per score name: count, mean and labels, for the list's filters. |
| `GET` / `POST /api/v1/score-configs` | A project's score configs; `PATCH /{id}` to change or archive one. |

### Score request

```http
POST /api/v1/trace-scores
```

```json
{
  "scores": [
    {
      "traceId": "4bf92f3577b34da6a3ce929d0e0e4736",
      "spanId": null,
      "name": "thumbs",
      "value": false,
      "comment": "blocked the wrong card",
      "source": "end_user",
      "externalId": "req-8841-3",
      "deploymentId": 12
    }
  ]
}
```

- `spanId` is `null` to score the whole trace, or one span's id.
- `value` is a number or `true`/`false`. A label goes in `stringValue` instead.
- `deploymentId` is only needed before the trace has arrived.

## Evaluators and monitors

| Endpoint | What it does |
| --- | --- |
| `GET` / `POST /api/v1/trace-evaluators` | A project's evaluators; `PATCH` and `DELETE /{id}`; `GET /templates` and `/variables`. |
| `POST /api/v1/trace-evaluators/{id}/run` | Judge one trace, span (`traceId`, `spanId`) or session (`sessionId`) now. |
| `POST /api/v1/trace-evaluators/{id}/backfills` | Judge a past window of up to 31 days; `GET` for progress, `POST /backfills/{id}/cancel` to stop. |
| `GET /api/v1/trace-evaluators/stats` | Label counts and mean score per evaluator over time. |
| `GET` / `POST /api/v1/trace-monitors` | A project's monitors; `PATCH` and `DELETE /{id}`; `GET /metrics`; `POST /preview` for a live value; `GET /{id}/events`; `POST /{id}/mute`, `/unmute`, `/acknowledge`. |
| `GET /api/v1/trace-findings` | Findings by project or asset, status, investigator and severity; `GET /counts`; `GET` and `PATCH /{id}` to change status or assignee; `POST /{id}/risk-assessment`. |

## Project settings

| Endpoint | What it does |
| --- | --- |
| `GET` / `POST /api/v1/trace-masking` | Read or replace a project's masking policy; `POST /test` tries a draft on sample text. |
| `GET` / `POST /api/v1/trace-dimensions` | A project's metadata dimension keys. |
| `GET` / `POST /api/v1/trace-views` | Saved views; `PATCH` and `DELETE /{id}`. |

## What to read next

- [Sending traces](../sending-traces/): the SDK and OTLP settings.
- [Scores and feedback](../scores-and-feedback/): what the score sources mean and who can edit them.
