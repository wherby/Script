from string import Template
RATE_TEXT='''
      <tr>
        <td>$id0</td>
        <td id='$id1'></td>
        <td id='$id2'></td>
        <td id='$id3'></td>
        <td id='$id4'></td>
        <td id='$id5'></td>
        <td id='$id6'></td>
      </tr>
			'''
RATETEMPLATE=Template(RATE_TEXT)
RATE_TEXT2=''''$ids','''
RATETEMPLATE2=Template(RATE_TEXT2)

actions=['PostBubble','PutBubble','GetBubble','CopyBubble','AsyncBubble','ABusEvent','CSEEvent']
endpoints=['endtoendv1','endtoendv2','endtoendv1Stag','endtoendv2Stag','endtoendv1Pro','endtoendv2Pro']
endpoints2=['endtoendeventv1','endtoendeventv2','endtoendeventv1Stag','endtoendeventv2Stag','endtoendeventv1Pro','endtoendeventv2Pro']


ids= range(7)
if __name__=="__main__":
    temp=""
    for action in actions:
        
        for i in range(len(endpoints)):
            ids[i]=endpoints[i]+action
            #print ids[i]
            b= {'ids':ids[i]}
            temp+= RATETEMPLATE2.safe_substitute(b)
        #a={'id0':action,'id1':ids[0],'id2':ids[1],'id3':ids[2],'id4':ids[3],'id5':ids[4],'id6':ids[5]}
        #print RATETEMPLATE.safe_substitute(a)
    print temp
            
