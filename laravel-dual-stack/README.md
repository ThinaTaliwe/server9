# Laravel Dual Stack

This stack creates two Laravel projects on one Docker Compose stack and connects both to one shared MySQL database.

- App 1: http://SERVER_IP:8081
- App 2: http://SERVER_IP:8082
- MySQL host port: 3307

Both apps use the same database but different table prefixes:
- app1_*
- app2_*
