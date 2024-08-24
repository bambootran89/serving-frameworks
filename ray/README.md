# Docs for Ray Serve
- https://docs.ray.io/en/latest/serve/getting_started.html

## Nhận xét: 
* Dễ sử dụng, linh hoạt trong thiết kế apis  
* Các dự án không yêu cầu tối ưu tốc độ có thể xem xét sử dụng ray 
* Không yêu cầu bất kì convert model nào trước khi sử dụng 
* Triển khai cùng với MLfLow dễ dàng 
bám sát hướng dẫn từ [MLflow Deployment](https://mlflow.org/docs/latest/deployment/index.html)
hoặc có thể tham khảo github [MLflow-Ray-Serve](https://github.com/ray-project/mlflow-ray-serve/blob/main/README.md), tuy nhiên bản này đã cũ và không thể chạy được với các phiên bản mới nhất. Tôi đã chỉnh lại toàn bộ code theo hướng dẫn mới nhất được đính kèm trong git này tại [updated MLflow-Ray-Serve](https://github.com/data-science-general-1/serving-frameworks/tree/main/ray/mlflow-ray-serve)

## Notes

+ [Ray Dashboard](https://docs.ray.io/en/latest/serve/monitoring.html): IP:8265

+  [The demo](https://github.com/data-science-general-1/mlflow-docker-server/blob/main/samples/deploy%20model-%20with%20rayml.ipynb) which is that Mlflow deploy a model

+ TODO: 
   + other features of rayml (Data, Train, Tune)
   + create slide guidelines 
   + generate more examples  
