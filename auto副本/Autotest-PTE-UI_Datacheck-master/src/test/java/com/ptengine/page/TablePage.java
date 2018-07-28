package com.ptengine.page;

import com.ptengine.base.BasePage;
import org.openqa.selenium.WebElement;
import org.openqa.selenium.support.CacheLookup;
import org.openqa.selenium.support.FindBy;

public class TablePage extends BasePage {
    @FindBy(className = "qa-tab-item-0")
    @CacheLookup
    public WebElement table_item_1;


    @FindBy(className = "qa-tab-item-1")
    @CacheLookup
    public WebElement table_item_2;

    @FindBy(className = "qa-table-head-col-url")
    @CacheLookup
    WebElement tablehead_OriginalPages;

    @FindBy(xpath = "/html/body/div[2]/div[1]/div[3]/div[2]/div/div/div/div[2]/div/div/div[2]/div/div/table/tbody/tr[4]/td[10]/div/a[2]/svg/use")
    @CacheLookup
    public WebElement icon_heatmap;



}
