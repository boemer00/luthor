# Luthor: A Legal RAG System

## Overview

Luthor is a Retrieval-Augmented Generation (RAG) system designed for law firms to enable lawyers to efficiently "talk to their data". This system allows legal professionals to upload documents (e.g., memos) to a vector database stored in Pinecone and subsequently query this information using a chatbot-like interface built with Streamlit.

## Features

- Document upload and processing (supports .txt, .pdf, and .docx files)
- Text preprocessing and segmentation
- Vector embedding generation using OpenAI's API
- Efficient document storage and retrieval using Pinecone
- Natural language querying interface
- Context-aware answer generation

## Components

1. **Data Loader** (`src/data_loader.py`): Handles reading various file formats.
2. **Preprocessor** (`src/preprocessor.py`): Prepares text for embedding and storage.
3. **Main Application** (`app.py`): Streamlit interface for document upload and querying.
4. **OpenAI Utilities**: Handles API interactions for embeddings and answer generation.
5. **Pinecone Utilities**: Manages vector database operations.

## System Architecture

Luthor is deployed on AWS using a containerized architecture:

- **Amazon ECS (Elastic Container Service)** with Fargate: Runs the Luthor application container.
- **Amazon ECR (Elastic Container Registry)**: Stores the Docker image for the Luthor application.
- **Application Load Balancer**: Distributes incoming traffic across multiple instances.
- **AWS Secrets Manager**: Securely stores and manages API keys.

## AWS Infrastructure

- ECS Cluster: Manages the Fargate tasks running the Luthor containers.
- ECR Repository: Hosts the Luthor Docker image.
- Application Load Balancer: Routes traffic to the ECS tasks.
- VPC and Security Groups: Provide network isolation and security.
- IAM Roles: Manage permissions for ECS tasks and other AWS services.

## Setup

### Prerequisites

- AWS Account
- AWS CLI configured with appropriate permissions
- Docker installed locally

### Installation

1. Clone the repository:
   ```
   git clone https://github.com/boemer00/luthor.git
   cd luthor
   ```

2. Build the Docker image:
   ```
   docker build -t luthor .
   ```

3. Push the image to Amazon ECR:
   ```
   aws ecr get-login-password --region [your-region] | docker login --username AWS --password-stdin [your-account-id].dkr.ecr.[your-region].amazonaws.com
   docker tag luthor:latest [your-account-id].dkr.ecr.[your-region].amazonaws.com/luthor:latest
   docker push [your-account-id].dkr.ecr.[your-region].amazonaws.com/luthor:latest
   ```

4. Set up AWS Secrets Manager:
   Create secrets for OPENAI_API_KEY, PINECONE_API_KEY, and PINECONE_ENVIRONMENT.

5. Deploy the ECS task definition:
   ```
   aws ecs register-task-definition --cli-input-json file://infrastructure/ecs-task-definition.json
   ```

6. Create an ECS service:
   ```
   aws ecs create-service --cluster [your-cluster-name] --service-name luthor-service --task-definition luthor-app --desired-count 1 --launch-type FARGATE --network-configuration "awsvpcConfiguration={subnets=[subnet-xxxxxxxx,subnet-yyyyyyyy],securityGroups=[sg-xxxxxxxxxxxxxxxx]}" --load-balancers "targetGroupArn=arn:aws:elasticloadbalancing:[region]:[account-id]:targetgroup/[target-group-name]/[target-group-id],containerName=luthor-app,containerPort=8501"
   ```

## Usage

Access the Luthor application through the Application Load Balancer's DNS name.

1. **Document Upload**:
   - Use the file uploader in the interface to upload legal documents (.txt, .pdf, or .docx).
   - The system will process the document, generate embeddings, and store them in Pinecone.

2. **Querying**:
   - Enter your legal query in the text input field.
   - Optionally, use the sidebar to refine your search by date range, document type, or legal area.
   - The system will retrieve relevant document chunks, generate an answer, and display it along with source information.

## Limitations and Future Improvements

- Currently, the system doesn't handle document deduplication effectively.
- The search refinement options (date range, document type, legal area) are not fully implemented in the backend.
- Error handling and logging could be improved for better debugging and user feedback.
- The system could benefit from more advanced NLP techniques for better understanding of legal context.
- Consider implementing auto-scaling for the ECS service based on traffic patterns.
- Implement a CI/CD pipeline for automated deployments.

## License

All rights reserved.

This code and all associated files are the exclusive property of Renato Boemer.
No part of this code, in any form or by any means, may be copied, reproduced, modified,
adapted, stored in a retrieval system, or transmitted without the prior written permission
of Renato Boemer.
