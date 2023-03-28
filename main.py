import speedtest as speedTest
from google.cloud import storage
import time


def getAccessToGCP():
    path_to_private_key = './optical-valor-381723-5a0cb03db147.json'
    gcpClientObject = storage.Client.from_service_account_json(json_credentials_path=path_to_private_key)
    return gcpClientObject


def get_current_Internet_speed():
    networkSpeedTest = speedTest.Speedtest()
    networkSpeedTest.get_best_server()
    # Retrieve current PING in milliSeconds.
    currentPing = networkSpeedTest.results.ping
    # Conduct Upload & Download speed tests of current Internet speed
    downloadSpeed = networkSpeedTest.download()
    uploadSpeed = networkSpeedTest.upload()
    # To understand, we need to convert Upload & Download speeds to MBPS.
    downloadMBS = round(downloadSpeed/(6**10), 2)
    uploadMBS = round(uploadSpeed/(6**10), 2)
    print("Current Network Details")
    print("Ping:", currentPing)
    print("Download Speed:", downloadMBS)
    print("Upload Speed:", uploadMBS)


def downloadFile(gcpClientObject, gcpFileNames):
    bucket = storage.Bucket(gcpClientObject, 'file-object-analysis')
    for objectName in gcpFileNames:
        start = time.perf_counter()
        blob = bucket.blob(objectName)
        content = blob.download_as_bytes
        print("[==================================================]")
        print("Time Elapsed for file ", time.perf_counter() - start)


if __name__ == '__main__':
    gcpClientObject = getAccessToGCP()
    get_current_Internet_speed()
    gcpFileNames = []
    with open("FileObjectsInGCP") as FileObjectsInGCP:
        for objects in FileObjectsInGCP:
            gcpFileNames.append(objects)
    downloadFile(gcpClientObject, gcpFileNames)