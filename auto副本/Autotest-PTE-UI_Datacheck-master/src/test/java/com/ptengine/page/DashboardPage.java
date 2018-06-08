package com.ptengine.page;

import com.ptengine.base.BasePage;
import org.openqa.selenium.WebElement;
import org.openqa.selenium.support.CacheLookup;
import org.openqa.selenium.support.FindBy;

import java.util.List;

public class DashboardPage extends BasePage {

    @FindBy(className = "qa-obase-vi")
    @CacheLookup
    public WebElement obase_vi;

    @FindBy(className = "qa-obase-uv")
    @CacheLookup
    public WebElement obase_uv;

    @FindBy(className = "qa-obase-pv")
    @CacheLookup
    public WebElement obase_pv;

    @FindBy(className = "qa-obase-anv-count")
    @CacheLookup
    public WebElement obase_newvi;

    @FindBy(className = "qa-obase-aov-count")
    @CacheLookup
    public WebElement obase_oldvi;


    @FindBy(className = "qa-obase-avi")
    @CacheLookup
    public WebElement obase_avi;

    @FindBy(className = "qa-obase-apv")
    @CacheLookup
    public WebElement obase_apv;

    @FindBy(className = "qa-obase-ast")
    @CacheLookup
    public WebElement obase_ast;

    @FindBy(className = "qa-obase-abr")
    @CacheLookup
    public WebElement obase_abr;

    @FindBy(className = "qa-sourcechart-item-percent-campaign")
    @CacheLookup
    public WebElement sourcechart_campaign;

    @FindBy(className = "qa-sourcechart-item-percent-referrer")
    @CacheLookup
    public WebElement sourcechart_referrer;


    @FindBy(className = "qa-sourcechart-item-percent-search")
    @CacheLookup
    public WebElement sourcechart_search;

    @FindBy(className = "qa-sourcechart-item-percent-social")
    @CacheLookup
    public WebElement sourcechart_social;

    @FindBy(className = "qa-sourcechart-item-percent-direct")
    @CacheLookup
    public WebElement sourcechart_direct;

    @FindBy(className = "qa-sourcechart-current-count")
    @CacheLookup
    public WebElement sourcechart_current_count;

    @FindBy(className = "qa-sourcechart-current-item-url")
    @CacheLookup
    public List<WebElement> sourcechart_current_url;

    @FindBy(className = "qa-sourcechart-current-item-v")
    @CacheLookup
    public List<WebElement> sourcechart_current_vi;

    @FindBy(className = "qa-os-list-li-keyword")
    @CacheLookup
    public List<WebElement> os_list_keyword;

    @FindBy(className = "qa-os-list-li-value")
    @CacheLookup
    public List<WebElement> os_list_vi;

    @FindBy(className = "qa-browser-item-keyword")
    @CacheLookup
    public List<WebElement> browser_list_keyword;

    @FindBy(className = "qa-browser-item-num")
    @CacheLookup
    public List<WebElement> browser_list_vi;


    @FindBy(className = "qa-pv-item-list-url")
    @CacheLookup
    public List<WebElement> pv_list_url;

    @FindBy(className = "qa-pv-item-list-heatmapbutton")
    @CacheLookup
    public List<WebElement> pv_list_heatmapbutton;

    @FindBy(className = "qa-pv-item-list-pagebutton")
    @CacheLookup
    public List<WebElement> pv_list_pagebutton;

    @FindBy(className = "qa-pv-item-list-num")
    @CacheLookup
    public List<WebElement> pv_list_pv;

    @FindBy(className = "qa-pv-item-detail")
    @CacheLookup
    public WebElement pv_item_detail;

    @FindBy(className = "qa-location-item-keyword")
    @CacheLookup
    public List<WebElement> location_item_keyword;

    @FindBy(className = "qa-location-item-value")
    @CacheLookup
    public List<WebElement> location_item_vi;

    @FindBy(className = "qa-location-item-detail")
    @CacheLookup
    public WebElement location_item_detail;



}
