import boto3
import pandas as pd


class Logs_Collector:
    def __init__(self, bucket=''):
        self.bucket = bucket
        self.s3_client = boto3.client('s3')

    def get_buckets_list(self):
        '''Get all buckets\' names list.'''
        response = self.s3_client.list_buckets()
        bucket_list = []
        ind = 0
        for bucket in response['Buckets']:
            ind+=1
            print(f'{ind}. {bucket["Name"]}')
            bucket_list.append(bucket["Name"])
        return bucket_list
    
    def get_logs_bucket(self):
        '''Get logs bucket by checking if any contains "loggging-test" string in it\'s name.'''
        bucket_list = self.get_buckets_list()
        for bucket in bucket_list:
            if 'logging-test' in bucket:
                return bucket
        return ''

    def set_logs_bucket(self, bucket):
        '''Reinitialize (set new) logs bucket or raise a value error if bucket\'s name is empty.'''
        if bucket == '':
            raise ValueError('Logs Bucket\'s name is empty!')
        else:
            self.bucket = bucket
            print(f'Logs Bucket set! Name: {bucket}')

    def get_log_objects(self):
        '''Get all objects from specified bucket (logs bucket) and return list of their keys.'''
        log_objects = []
        paginator = self.s3_client.get_paginator('list_objects_v2')
        operation_parameters = {'Bucket': self.bucket}
        page_iterator = paginator.paginate(**operation_parameters)
        for page in page_iterator:
            # print(page['Contents'])
            key_list = page['Contents']
            for key in key_list:
                log_objects.append(key['Key'])
        return log_objects

    def get_log_data_in_DF(self):
        '''Get log data from logs bucket and convert it into Pandas DataFrame format.'''
        log_objects = self.get_log_objects()
        log_data = []
        for log_key in log_objects:
            log_data.append(pd.read_csv('s3://' + self.bucket + '/' + log_key, sep = " ", names=['Bucket_Owner', 'Bucket', 'Time', 'Time_Offset', 'Remote_IP', 'Requester_ARN/Canonical_ID',
                    'Request_ID',
                    'Operation', 'Key', 'Request_URI', 'HTTP_status', 'Error_Code', 'Bytes_Sent', 'Object_Size',
                    'Total_Time',
                    'Turn_Around_Time', 'Referrer', 'User_Agent', 'Version_Id', 'Host_Id', 'Signature_Version',
                    'Cipher_Suite',
                    'Authentication_Type', 'Host_Header', 'TLS_version'],
                usecols=[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24]))
        logs_df = pd.concat(log_data)
        logs_df.info()
        return logs_df

    def download_log_file(self, log_name, filename):
        '''Download specified log file from logs bucket.'''
        with open(filename, 'wb') as f:
            self.s3_client.download_file(self.bucket, log_name, f)
        print('get logs function')


# def main():
#     logs_collector = Logs_Collector()
#     logs_collector.set_logs_bucket(logs_collector.get_logs_bucket())



# if __name__ == "__main__":
#     main()