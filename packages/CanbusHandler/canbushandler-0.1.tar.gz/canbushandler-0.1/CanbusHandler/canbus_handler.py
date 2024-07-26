import can
import threading
import time

class Channel:
    CanA = 0
    CanB = 1

class WriteMessage:
    def __init__(self, pid:int, message:list, times:int):
        self.pid     = pid
        self.message = message
        self.times   = times

class ReadMessage:
    def __init__(self, pid:int, offset:int, len:int, alias:str):
        self.alias  = alias
        self.pid    = pid
        self.offset = offset
        self.len    = len
        self.value  = 0

class Handler:
    def __init__(self, channel:int):
        self.Canbus = can.interface.Bus(channel=f'can{channel}', bustype='socketcan')
        self.listOfMessagesToSend = [] 
        self.listOfMessagesToRead = [] 

    def GetValue(self, alias:str):
        for message in self.listOfMessagesToRead:
            if(message.alias == alias):
                return message.value
        return 0

    def AddCheckList(self, pid:int, offset:int, len:int, alias:str):
        self.listOfMessagesToRead.append( ReadMessage(pid, offset, len, alias) )

    def SendMessage(self, pid:int, message:list, times:int):
        self.listOfMessagesToSend.append( WriteMessage(pid,message,times) )

    def CancelMessage(self, pid:int):
        for i in range(len(self.listOfMessagesToSend)):
            if(self.listOfMessagesToSend[i].pid == pid):
                self.listOfMessagesToSend.pop(i)

    def MessageSender(self):
        while True:
            i=0
            while i < len(self.listOfMessagesToSend):
                # get message object
                msg = self.listOfMessagesToSend[i]

                # check are permanent message
                if msg.times != -1:
                    msg.times -= 1

                # send message to canbus
                self.Canbus.send(can.Message(arbitration_id=msg.pid, data=msg.message, is_extended_id=False))

                # if delete index, not need move index
                if(msg.times == 0):
                    self.listOfMessagesToSend.pop(i)
                else:
                    i+=1
            time.sleep(1)

    def GetValueByCanMsg(msg:list, offset:int, length:int):
        returnStr = ""
        for i in msg:
            # Convert every index to 00101001 format
            returnStr += format(int(i), '08b')
        if (offset + length) < len(returnStr):
            return int(returnStr[offset : (offset+length)])
        else:
            return -1

    def ReceiveMessage(self):
        while True:
            try:
                message = self.Canbus.recv()
                if message:
                    for variable in self.listOfMessagesToRead:
                        if message.arbitration_id == variable.pid: 
                            newValue = self.GetValueByCanMsg(message.data,variable.offset,variable.length)
                            if(newValue != variable.value):
                                variable.value = newValue
                                print(f"Variable {variable.alias} updated to {newValue}")

            except can.CanError as e:
                print(f"Error receiving message: {e}")

    def Begin(self):
        if self.Canbus is None:
            raise RuntimeError("Interface need init first!")
        
        Canbus_SendThread = threading.Thread(target=self.MessageSender)
        Canbus_ReceiveThread = threading.Thread(target=self.ReceiveMessage)

        Canbus_SendThread.start()
        Canbus_ReceiveThread.start()

        Canbus_SendThread.join()
        Canbus_ReceiveThread.join()

        self.Canbus.shutdown()