# Whiplash

Serverless, lightweight, and fast vector store on top of DynamoDB

## Description

Whiplash is a lightweight vector store built on top of [AWS DynamoDB](https://aws.amazon.com/dynamodb/). It uses a variant of [locality-sensitive hashing (LSH)](https://en.wikipedia.org/wiki/Locality-sensitive_hashing) to index vectors in a DynamoDB table. This is intended to be a mimimalist, scalable, and fast vector store and is intended to be extremely easy to use, maintain, and self-host.

### Common Deployment Modifications

 - To add a (pretty) domain name to the API, set "domain": "your_domain_name" in the apigw component
 - To change the region from the default set the CloudKommand project to be in a different region
 - To change the stage (dev vs qa vs prod) set the environment variable in the API Lambda