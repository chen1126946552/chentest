package com.ptengine.page;

import com.ptengine.base.BasePage;
import org.openqa.selenium.WebElement;
import org.openqa.selenium.support.CacheLookup;
import org.openqa.selenium.support.FindBy;

public class HeatmapPage extends BasePage {

    @FindBy(xpath = "//*[@id=\"js-heatmap-count\"]/div/span[1]/span")
    @CacheLookup
    public WebElement clicknum;

    @FindBy(xpath = "//*[@id=\"js-heatmap-count\"]/div/span[2]/span")
    @CacheLookup
    public WebElement pvnum;

    @FindBy(xpath = "//*[@id=\"js-heatmap-count\"]/div/span[3]/span")
    @CacheLookup
    public WebElement vinum;

}
