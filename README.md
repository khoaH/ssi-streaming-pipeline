
# SSI Stock Data Streaming Pipeline

A stock data streaming pipeline from SSI's iboard. This project's main purpose is to get my hands dirty on a real Data Engineering work. Beside that, it showcases streaming pipeline development with scalability and availability.

***Important Notes***: 
* This project's data source is the [iboard](https://iboard.ssi.com.vn/) website's websocket. Therefore, any changes that was made to its data output in the future will break this pipeline.
* Iboard's web-UI will close the socket and create new one after not receiving messages for a few minutes. This behavior will likely break the pipeline. Reconnecting or Scheduling will be added in future development.
## Acknowledgements
This project was inspired by:
 - [Finnhub Streaming Data Pipeline](https://github.com/RSKriegs/finnhub-streaming-data-pipeline)

## Architecture Diagram

![Data Streaming Pipeline](https://raw.githubusercontent.com/khoaH/ssi-streaming-pipeline/master/ssi-pipeline.png)      
    
### **Data Source**: 
After researching for sometimes, the SSI's iboard provided to be the most fit for my project. SSI already has its own API but this requires some registrating work and at the time i don't really have the resources for that. You can read more about that [here](https://www.ssi.com.vn/khach-hang-ca-nhan/fast-connect-api).   

### **Data Ingestion**: 
In order to subcribe to specific tickers the websocket server, you need to use SSI's specific stock IDs. You can't use their symbols. I've created a dictionary for all of their stocks. Therefore you only need to modify the stocks you want in the ```ssi-producer/src/settings.json```.   

After sending the required messages to the socket, the server will send the stock data in a single line with '|' separator. Example:
```
S#hose:1354|HPG|20800|17700|20650|58100|20600|202500||||...
```
This however, doesn't inlude any timestamp. Therefore, before sending the data to the Message Broker, a time stamp need to be added.
```
{"timestamp": 1682670050.3190935, "message": "S#hose:1354|HPG|20900|163800|20850|133200|20800|131500|..."}
```

### **Message Streaming**:
Since scalability and availabity was a thing to keep in mind, a message broker was required. This is processed via **Apache Kafka**.

### **Data Transformation**:
All the data will be transformed using pySpark (Apache Spark's python API) with the use of clustering. Transformed data will be push into their respective table in the database.

### **Serving Database**:
Processed data will be stored inside a Cassandra database. Cassandra was chosen because it provides an excellent way to store time serires data and expand if needed.   

Example Table:
```
trades(
    uuid uuid,
    trade_timestamp timestamp,
    session text,
    symbol text,
    price double,
    traded_volume int,
    diff_percentage float,
    diff_value float,
    total_volume int,
    total_value int,
    PRIMARY KEY((symbol), trade_timestamp))
```
### **Visualization**:
Grafana was chosen as a visualization tool as they provide a wide range of support and multiple plugins.
## Prerequisites

Docker and Docker Compose plugin are required to run this project.
* [Docker](https://docs.docker.com/engine/install/)
* [Docker Compose](https://docs.docker.com/compose/install/)
## Deployment

To deploy this project, run this command at the project location

```bash
    docker compose up -d
```

Keep in mind that both the Ho Chi Minh and Hanoi Stock Exchange open at 9:00 AM UCT+7. Deploying the pipeline outside of this timeline won't yield any data.
* If you're experencing slow deployment result in not having any data, this could be because Spark deployment had some issues. You can restart its container by running:
``` bash
    docker compose restart spark-process
```
## Dashboard Example

Visit [localhost:3000](localhost:3000) after deployment to see the dash board.

**Note**: Web UI setup can take awhile. Refresh everyfew minutes after deployment.

![Dashboard](https://raw.githubusercontent.com/khoaH/ssi-streaming-pipeline/master/dashboard.png)

## Teardown 

To teardown resources run
``` bash
    docker compose down
```
## Future Work

This project has a lot of room to improve. For the time being, however, i would like this to be a hands-on project to teach me about the underlying technical aspects of a modern streaming data stack. Unfortunately, i think this will need to be set aside for now since i really want to dip my hands into practical data engineering - doing real work in a job. I'll definitely go back and give this project a future look if i have the time.
That aside, here are some future works i could do to improve this project:
* *Persistant Storage for all container*: Providing persistant storage for some of the elements turned out to be more difficult than expected. I will update this when i learned Terraform or other IaC tools in the future to utilize hardware more consistently.
* *Schedule/Reconnection for producer*: This should be the number one priority for this project since it make use of an unstable data source. Scheduling the producer to run at 9:00AM-11:30AM and 1:00PM-3:00PM from Monday to Friday would be the ideal solution. Reconnecting need to be added but this was proven to be above my skill level for now. It requires much more understanding of websocket/docker. I'll come back to this but scheduling should provide an excellent way to mitigate breaking connection with the socket.
* *Cloud deployment*: Before i opted for deploying this project locally, i considered a lot of the cloud-based option. There are free Cloud servers to try out but i'd rather stick to locally. Deployinng locally would make this project easier to control and less of a finacial risk if i make any miscalculation on Cloud's pricing. Moreover, deploying this project in the cloud should be a similar task since it is all containerized via Docker Compose.
* *CI/CD pipeline*: A CI/CD pipeline should be used to ensure the project will be easy to test and review.
## License

[MIT](https://github.com/khoaH/ssi-streaming-pipeline/blob/8586fb94d7c07166156f6acd2c2f7e57a9ccd117/LICENSE/)

