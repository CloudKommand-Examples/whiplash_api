# Whiplash

Serverless, lightweight, and fast vector store on top of DynamoDB

## Description

Whiplash is a lightweight vector store built on top of [AWS DynamoDB](https://aws.amazon.com/dynamodb/). It uses a variant of [locality-sensitive hashing (LSH)](https://en.wikipedia.org/wiki/Locality-sensitive_hashing) to index vectors in a DynamoDB table. This is intended to be a mimimalist, scalable, and fast vector store and is intended to be extremely easy to use, maintain, and self-host.

## Deployment and Usage

We recommend that you clone this Github template into a personal workspace or organization within Github.

The API is deployed using [CloudKommand](https://cloudkommand.com), and it uses API Key authentication, which must be set in the project's secrets before deploying.

The fundamental units in Whiplash are collections and items, where an item is a vector, and a collection is a set of items that are indexed for fast search. Default settings for collections
are set during deployment, but all settings can be changed when creating a collection.

### Common Deployment Modifications (Within CloudKommand)

 - To add a (pretty) domain name to the API, set "domain": "your_domain_name" in the apigw component
 - To change the region from the default set the CloudKommand project to be in a different region
 - To change the default values for collections, override the environment variables in the api_lambda component
 - To change the stage (dev vs qa vs prod), set the STAGE environment variable in the api_lambda component