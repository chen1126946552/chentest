package com.listener;

import net.gpedro.integrations.slack.SlackApi;
import net.gpedro.integrations.slack.SlackAttachment;
import net.gpedro.integrations.slack.SlackMessage;

import java.util.Collections;

public class SlackMessageSend {
    public void sendWithAttachment(String link,String text,SlackAttachment attachment){
        try{
            SlackMessage slackMessage = new SlackMessage();
            slackMessage.setLinkNames(true);
            slackMessage.setChannel("@ptmind-cn-qa");
            slackMessage.setAttachments(Collections.singletonList(attachment));
            slackMessage.setText(text);
            SlackApi sa=new SlackApi(link);
            sa.call(slackMessage);
        }catch (Exception e){
            e.printStackTrace();
        }
    }
}
