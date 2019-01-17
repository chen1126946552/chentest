package com.listener;

import net.gpedro.integrations.slack.SlackAttachment;
import net.gpedro.integrations.slack.SlackField;

import java.util.Objects;

public class SlackAttachmentBuild {

    public SlackAttachment newAttachment(String title, String text){
        SlackAttachment slackAttachment = new SlackAttachment();
        slackAttachment.setFallback("@channel");
        slackAttachment.setColor("#FF0000");
//        slackAttachment.setFields(testtttt);
//        slackAttachment.addMarkdownAttribute("@channel");
        slackAttachment.setTitle(title);
//        slackAttachment.setTitleLink(titleLink);
        slackAttachment.setText(text);
        slackAttachment.setAuthorName("wang.yao");
        slackAttachment.setImageUrl("@channel");
        return slackAttachment;
    }

    public static SlackField newField(String name, Object value){
        SlackField field = new SlackField();
        field.setTitle(name);
        field.setValue(Objects.toString(value));
        field.setShorten(false);
        return field;
    }
}
