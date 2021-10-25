# PyDM
다수의 태스크를 워커에 분배해 처리하는 모듈

- Distributor : 태스크를 Worker에 할당
- Worker : 태스크를 처리
- Monitor : 태스크 처리 결과 조회

<img src="https://i.imgur.com/GdlZe7g.png" alt="00" style="zoom: 67%;" />



## 사용법

### config 작성

distributor와 worker를 사용하기 위해서는 `.dm`에 정보를 입력해야한다. 각 포트는 중복되지 않는 값을 지정한다.

```
WORKER_NAME=worker1
DISTRIBUTOR_HOST=localhost
RESOURCE_PORT=53000
TASK_PORT=53001
MONITOR_PORT=53002
DISTRIBUTOR_REP_PORT=53004
```

- WORKER_NAME : 워커일 경우 워커의 이름 지정
- DISTRIBUTOR_HOST : Distributor가 동작하는 머신에 접속하기 위한 호스트
- RESOURCE_PORT : Worker의 리소스 사용량을 전송할 포트
- TASK_PORT : 태스크 할당에 사용할 포트
- MONITOR_PORT : 모니터 모듈에 정보를 전달할 포트
- DISTRIBUTOR_REP_PORT : Distributor에 메세지를 지정하는 포트

### Distributor

`DM.Distributer`를 상속해 분배기 코드 정의

아래의 함수들을 재정의 해서 사용할 수 있다.

- `pre_task_send` : Worker로 Task 전달 시 호출됨
- `pre_task_start` : Worker에서 작업 처리 시작 시 호출됨
- `pre_task_end` : Worker에서 작업이 완료된 이후 호출됨

#### example

```python
class MyDistributor(Distributor):

    def __init__(self):
        super().__init__()

    def pre_task_send(self, worker, task_id, task_info):
        print("태스크 전송 시작")

    def pre_task_start(self, task_id, task):
        print("워커에서 태스크 시작")

    def pre_task_end(self, task_id, task, result):
        print("태스크 처리 완료")


if __name__ == "__main__":
    zd = MyDistributor()
    zd.run()                
```

### Worker

작업을 수행할 클래스를 작성한다. 클래스는 **ModuleWrapper** 클래스를 상속해 만들 수 있다.

- `pre_work` : 작업 시작 전 호출됨
- `post_work` : 작업 종료 후 호출됨
- `work` : 수행할 작업을 작성한다.

#### example

```python
from DM.ModuleWrapper import ModuleWrapper


class MyWorker(ModuleWrapper):

    def pre_work(self):
        print("pre_work in MyWorker")

    def post_work(self):
        print("post_work in MyWorker")

    def work(
        self,
        value1,
        value2
    ):
        return value1 + value2
```

### Caller

Distributor와 Worker가 구동중 일 때 **DM.Caller**를 통해 작업을 요청할 수 있다.

#### example

```python
Caller.call("mllibra.sogang.ac.kr", 53004, value1=10, value2=20)
```



## Monitoring

![01](https://i.imgur.com/KiyMPBt.png)

flask 기반 모니터링 웹 페이지 사용 가능

