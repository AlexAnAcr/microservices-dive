import ServerAPI

serv = ServerAPI.MicroService(url_get='http://localhost:8080/got',
                                   url_post='http://localhost:8080/gave',
                                   persistentMode=True)

while True:
    first_data,addr = serv.GetNextJob(job_type='Demo.Backend.MutliExpressionCalculator.EffectiveManager')

    second_data = serv.ProcessAsFunction(content=first_data,
                           requested_function='Demo.Backend.LineTrimmer')

    third_data = serv.ProcessAsFunction(content=second_data,
                           requested_function='Demo.Backend.MutliExpressionCalculator.LinesProcessor')

    serv.PostFinalResult(content=third_data,
                         result_type='Demo.Backend.MutliExpressionCalculator.EffectiveManager.Merit',
                         responseAddress=addr)
