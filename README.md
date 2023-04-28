
# SSI Stock Data Streaming Pipeline

A stock data streaming pipeline from SSI's iboard. This project's main purpose is to get my hands dirty on a real Data Engineering work. Beside that, it showcases streaming pipeline development with scalability and availability.

***Important Notes***: 
* This project's data source is the [iboard](https://iboard.ssi.com.vn/) website's websocket. Therefore, any changes that was made to its data distribution method will break this pipeline.
* Iboard's web-UI will break the socket and create new one after not receiving messages for a few minutes. **Reconnect after closed** was considered as a solution but **Scheduling** should be a better method. I'll add this in future development.
## Acknowledgements
This project was deeply inspired by:
 - [Finnhub Streaming Data Pipeline](https://github.com/RSKriegs/finnhub-streaming-data-pipeline)

## Architecture Diagram

![Data Streaming Pipeline](https://raw.githubusercontent.com/khoaH/ssi-streaming-pipeline/master/ssi-pipeline.png)      
    
### **Data Source**: 
After researching for sometimes, the SSI's iboard provided to be the most fit for my project. There is already a stock data api from SSI itself but this requires some registrating work. You can read more about that [here](https://www.ssi.com.vn/khach-hang-ca-nhan/fast-connect-api).   

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
Because scalability and availabity was a thing to keep in mind, a message broker was required to make the pipeline scalable. This was done using **Apache Kafka**.

### **Data Transformation**:
All the data will be processed via a Spark cluster for easy scaling, using pySpark API. Transformed data will be push into their respective table in the database.

### **Serving Database**:
Processed data will be stored inside a Cassandra database. Cassandra was chosen because it provides and excellent way to store time serires data and easiness of scaling.   

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
Grafana will be the chosen as a visualization tool as they provide a wide range of support and multiple plugins.
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
* If you're experencing slow deployment result in not having any data, this could be because Spark deployment had some issues. You can restart the specific container by running:
``` bash
    docker compose restart spark-process
```
## Dashboard Example

Visit [localhost:3000](localhost:3000) after deployment to see the dash board.

**Note**: Web UI setup can take awhile. Refresh everyfew minutes after deployment.

![Dashboard](https://raw.githubusercontent.com/khoaH/ssi-streaming-pipeline/master/dashboard.png)

## Teardown Infra

To teardown resources run
``` bash
    docker compose down
```
## Future Work

I know for a fact that this project has a lot of room to improve. However, i would like this to be a hands-on project to enlighten me about the underlying technical aspect of a modern streaming data stack.    
Unfortunately, that is the reason why i will only update this project if i have the free time. I would like to build more impactful projects that provide real value to others. 
That aside, here some aspect i could improve:
* *Persistant Storage for all container*: Providing persistant storage for some of the applications turned out to be more strange than expected. I will update this when i learned Terraform in the future to utilize hardware more consistently.
* *Scheduling and reconnect for producer*: As said in previous section, this project use an unstable data source. I chosed because it provided me an excellent challenge in understanding websocket. Scheduling the producer to run at 9:00AM-11:30AM and 1:00PM-3:00PM from Monday to Friday would be the ideal solution. Adding a reconnection function won't be neccessary since the PySpark script included some filtering.
* *Cloud deployment*: Before i opted for deploying this project locally, i considered a lot of the cloud based option. However, it would be a big financial issue since i'm relatively new to Cloud Server's pricing. Beside, deploying this project in the cloud won't be a difficult task since it is all containerized.
* *CI/CD pipeline*: A CI/CD pipeline should be used to ensure the project free of deploying errors.
## License

[MIT](https://choosealicense.com/licenses/mit/)

