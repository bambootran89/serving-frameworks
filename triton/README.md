# Docs for DS Triton
- https://github.com/triton-inference-server/fil_backend

## Nhận xét: 
### Ứu điểm  
  * Hỗ trợ nhiều định dạng, backendend model
  * Triển khai cùng với MLfLow dễ dàng  bám sát hướng dẫn từ [MLflow Deployment](https://mlflow.org/docs/latest/deployment/index.html)
  hoặc có thể tham khảo github [MLflow-MLflow Triton](https://github.com/triton-inference-server/server/tree/main/deploy/mlflow-triton-plugin#mlflow-triton), tuy nhiên bản này đã cũ và không thể chạy được với các phiên bản mới nhất. Tôi đã chỉnh lại toàn bộ code theo hướng dẫn mới nhất được đính kèm trong git này tại [updated MLflow Triton](https://github.com/data-science-general-1/serving-frameworks/tree/main/triton/mlflow-triton-plugin)
  * api hỗ trợ grpc và https + nhiều phương thức bảo mật 

### Nhược điểm: 
  * ONNx được hỗ trợ tối đa còn lại thì ít được hỗ trợ hơn khi muốn deploy cùng với S3, kết hợp với công cụ tiên tiên như MLflow.
  * Các mô hình đòi hỏi phải được convert về định đạng được support trước khi deploy 



## Notes

+ Port: HTTP requests (port 8000),GRPC requests (port 8001),Prometheus metrics (port 8002) 

+ [The demo](https://github.com/data-science-general-1/mlflow-docker-server/blob/main/samples/mlflow-2-serving%20-%20with%20triton.ipynb) which is that Mlflow deploy a model

+ TODO: 
   + create slide guidelines 
   + generate more examples  