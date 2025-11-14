**EMR API – DevOps Practical Project**

This is a small Electronic Medical Records (EMR) API I worked on to improve my DevOps skills. I wanted to take a simple Python API and make it production-ready using Docker, Kubernetes, and proper monitoring. The whole idea was to practice how real-world healthcare applications are packaged, deployed, and observed.

**What I Built**

I containerized the API using Docker, wrote the Kubernetes manifests myself, and added Prometheus so I can scrape metrics from the service. I set this up as part of my journey to understand how DevOps and MLOps pipelines are built end-to-end.
This helped me see how an app moves from local development → container → cluster → monitoring.

**Tech Stack I Used**

Python – Basic API logic

Docker – Image building and running the service locally

Kubernetes (k8s) – Deployment and Service files for running it in a cluster

Prometheus – Collecting metrics from the API

Grafana – For dashboarding (optional for now)

**How I Run the Project**

When I’m testing locally, I normally use Docker Compose:

docker-compose up --build


For Kubernetes, I apply the files in the k8s folder:

kubectl apply -f k8s/
kubectl get pods
kubectl get svc


Prometheus will pick up the metrics based on the config in prometheus.yml.

**What I Learned**

Working on this project helped me understand:

How to containerize a Python API cleanly

How Kubernetes Deployments and Services work together

How to expose and scrape metrics with Prometheus

How DevOps workflows support real applications like EMR systems

This project is part of my bigger plan to build a full DevOps/MLOps portfolio and become very strong in real-world cloud engineering.
