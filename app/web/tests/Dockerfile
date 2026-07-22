FROM mcr.microsoft.com/playwright:v1.55.0-noble
WORKDIR /tests
COPY package.json ./
RUN npm install --no-audit --no-fund
COPY playwright.config.mjs adoption-flow.spec.mjs ./
