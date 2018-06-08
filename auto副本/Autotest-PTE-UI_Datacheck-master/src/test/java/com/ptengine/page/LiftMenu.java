package com.ptengine.page;

import com.ptengine.base.BasePage;
import org.openqa.selenium.WebElement;
import org.openqa.selenium.support.CacheLookup;
import org.openqa.selenium.support.FindBy;

public class LiftMenu extends BasePage {

    @FindBy(className = "qa-pt-btn-nav-overview")
    @CacheLookup
    WebElement menu_Dashboard;

    @FindBy(className = "qa-pt-btn-nav-source")
    @CacheLookup
    WebElement menu_Source;

    @FindBy(className = "qa-pt-btn-subnav-overview")
    @CacheLookup
    WebElement menu_Source_overview;

    @FindBy(className = "qa-pt-btn-subnav-campaign")
    @CacheLookup
    WebElement menu_Source_campaign;

    @FindBy(className = "qa-pt-btn-subnav-referral")
    @CacheLookup
    WebElement menu_Source_referral;

    @FindBy(className = "qa-pt-btn-subnav-search_engine")
    @CacheLookup
    WebElement menu_Source_search_engine;

    @FindBy(className = "qa-pt-btn-subnav-search_terms")
    @CacheLookup
    WebElement menu_Source_search_terms;

    @FindBy(className = "qa-pt-btn-subnav-social_site")
    @CacheLookup
    WebElement menu_Source_social_site;

    @FindBy(className = "qa-pt-btn-nav-content")
    @CacheLookup
    public WebElement menu_Content;

    @FindBy(className = "qa-pt-btn-subnav-page")
    @CacheLookup
    public WebElement menu_Content_page;

    @FindBy(className = "qa-pt-btn-subnav-page_group")
    @CacheLookup
    WebElement menu_Content_page_group;

    @FindBy(className = "qa-pt-btn-subnav-entry_page")
    @CacheLookup
    public WebElement menu_Content_entry_page;

    @FindBy(className = "qa-pt-btn-nav-technology")
    @CacheLookup
    WebElement menu_Technology;

    @FindBy(className = "qa-pt-btn-subnav-overview")
    @CacheLookup
    WebElement menu_Technology_overview;

    @FindBy(className = "qa-pt-btn-subnav-device")
    @CacheLookup
    WebElement menu_Technology_device;

    @FindBy(className = "qa-pt-btn-subnav-os")
    @CacheLookup
    WebElement menu_Technology_os;

    @FindBy(className = "qa-pt-btn-subnav-browser")
    @CacheLookup
    WebElement menu_Technology_browser;

    @FindBy(className = "qa-pt-btn-subnav-resolution")
    @CacheLookup
    WebElement menu_Technology_resolution;


}
