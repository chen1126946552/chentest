package bin;

import java.io.File;
import java.io.FileNotFoundException;
import java.io.FileOutputStream;
import java.io.OutputStreamWriter;
import java.io.UnsupportedEncodingException;
import java.util.List;
import org.dom4j.Attribute;
import org.dom4j.Document;
import org.dom4j.Element;
import org.dom4j.io.SAXReader;

public class xml2csv {
	public  void writecsv(String infile,String outfile) throws Exception {
		SAXReader reader = new SAXReader();
		File file = new File(infile);
		Document document = reader.read(file);
		Element root = document.getRootElement();
		List<Element> childElements = root.elements("httpSample");
		OutputStreamWriter out = null;
		try {
			out = new OutputStreamWriter(new FileOutputStream(outfile), "utf8");
		} catch (UnsupportedEncodingException e) {
			e.printStackTrace();
		} catch (FileNotFoundException e) {
			e.printStackTrace();
		}
		for (Element child : childElements) {
			out.write(child.attributeValue("lb") + "\t" + child.attributeValue("tn") + "\t"
					+ child.elementText("responseData").substring(1,child.elementText("responseData").length()-1) + "\n");
		}
		out.close();
	}
	
	public void writefile(String filepath,String path,String content) throws Exception{
		OutputStreamWriter out = null;
		try {
			out = new OutputStreamWriter(new FileOutputStream(filepath), "utf8");
			out.write(path+content);
			out.flush();
		} catch (UnsupportedEncodingException e) {
			e.printStackTrace();
		} catch (FileNotFoundException e) {
			e.printStackTrace();
		}
		out.close();
	}
	
	public void delFile(String filepath)throws Exception{
        File file=new File(filepath);
        if(file.exists()&&file.isFile())
            file.delete();
    }
}