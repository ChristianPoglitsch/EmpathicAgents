# LLM Communication System

## Overview

This folder contains the code for interacting with both OpenAI and local language models (LLMs). It provides abstractions for sending text prompts and retrieving embeddings from models. The system is divided into two primary communication modules: one for interacting with OpenAI's API and another for working with locally hosted models.

## Modules

### 1. `OpenAIComms`

Handles communication with OpenAI's models for chat completions and embeddings.

- Send chat messages to OpenAI models.
- Retrieve text embeddings from OpenAI models.
- Configurable parameters for API requests, including temperature, max tokens, and penalties.

### 2. `LocalComms`

Interfaces with local models, including HuggingFace models and Sentence Transformers.

- Load and interact with local models for text generation and embeddings.
- Supports fine-tuned models loaded from a local directory.
- Configurable parameters for text generation.

