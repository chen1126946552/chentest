package com.ptengine.pagemethod;

import com.ptengine.page.HeatmapPage;

public class HeatmapMethod extends HeatmapPage {

    public int getClicknum() {
        return Integer.parseInt(clicknum.getText().replace(",", ""));
    }

    public int getPVnum() {
        return Integer.parseInt(pvnum.getText().replace(",", ""));
    }

    public int getVInum(){
        return Integer.parseInt(vinum.getText().replace(",",""));
    }
}
