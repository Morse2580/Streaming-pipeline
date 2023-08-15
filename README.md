# Streaming-pipeline
Finnhub Streaming Data Pipeline
The project is a streaming data pipeline based on Finnhub.io API/websocket real-time trading data created for a sake of my master's thesis related to stream processing. It is designed with a purpose to showcase key aspects of streaming pipeline development & architecture, providing low latency, scalability & availability.

The repo is based of an idea of decomposing Large Scale Data Systems. The premise behind this is that the 
`Key to understanding 𝗟𝗮𝗿𝗴𝗲 𝗦𝗰𝗮𝗹𝗲 𝗗𝗮𝘁𝗮 𝗦𝘆𝘀𝘁𝗲𝗺𝘀 is the ability to 𝗗𝗲𝗰𝗼𝗺𝗽𝗼𝘀𝗲 𝘁𝗵𝗲𝗺 𝗶𝗻𝘁𝗼 𝘀𝗺𝗮𝗹𝗹𝗲𝗿 𝗙𝘂𝗻𝗱𝗮𝗺𝗲𝗻𝘁𝗮𝗹 𝗽𝗶𝗲𝗰𝗲𝘀.`

---
### Architecture and concepts
This concept is inspired by [Aurimas Griciūnas](https://www.linkedin.com/in/aurimas-griciunas/). 
You can subscribe to his newsletter, He offers valuable information on real-world data engineering and MLOps systems. (not sponsored!)

![aurimas.png](readme-images%2Faurimas.png)



---
### Project inspiration
The project itself is inspired by [TheAlgorist](https://github.com/The-Algorist/finnhub-streaming-data-pipeline/tree/main),
He carefully crafts his code, in an understandable manner.

![algoris.png](readme-images%2Falgoris.png)


---

`NB: Architecture will be broken down within each module of the project`
- The initial step will be to deploy the application locally
- Ònce I have successfully deployed the project locally, I can the deploy it on a cloud provider using [Pulumi](https://www.pulumi.com/docs/) for Iac


