package main

import (
	"bufio"
	"fmt"
	"io"
	"io/ioutil"
	"log"
	"os"
	"path"
	"strings"

	"github.com/PuerkitoBio/goquery"
	"github.com/otiai10/copy"
	"github.com/yosssi/gohtml"
)

/////////////////////////////////////
// Paths and Directories
/////////////////////////////////////

var (
	goldenRoot = "golden/"
	leRoot     = "resources/website/"
	leImages   = "resources/website/static/images/"
)

/////////////////////////////////////
// Main Functions
/////////////////////////////////////

// Copy source directory to destination
func placeDirectory(srcDir, destDir string) error {

	// if directory not exists copy srcDir to destDir
	fileInfo, err := os.Stat(destDir)

	if os.IsNotExist(err) {

		err = copy.Copy(srcDir, destDir)

		if err != nil {
			return err
		}

		fmt.Println(destDir + " directory created successfully!")
		return nil
	}

	// if directory exists, replace it
	err = os.RemoveAll(destDir)
	if err != nil {
		return err
	}

	err = copy.Copy(srcDir, destDir)

	if err != nil {
		return err
	}

	fmt.Println(fileInfo.Name() + " directory updated successfully!")
	return nil
}

// delete a directory
func deleteDirectory(rmDir string) error {
	fileInfo, err := os.Stat(rmDir)

	if os.IsNotExist(err) {
		return nil
	}

	err = os.RemoveAll(rmDir)

	if err != nil {
		return err
	}

	fmt.Println(fileInfo.Name(), "directory deleted successfuly!")
	return nil
}

// placeFile move file from srcFile to destFile
func placeFile(fileName, srcFile, destFile string) (int64, error) {

	f, err := os.Open(srcFile)
	defer f.Close()

	if err != nil {
		return 0, err
	}

	d, err := os.Create(destFile)
	defer d.Close()

	if err != nil {
		return 0, err
	}

	return io.Copy(d, f)
}

// replaceString
func replaceString(file, oldLine, newLine string) error {

	data, err := ioutil.ReadFile(file)

	if err != nil {
		return err
	}

	updatedData := strings.Replace(string(data), oldLine, newLine, -1)

	return ioutil.WriteFile(file, []byte(updatedData), 0660)

}

// delete html element
// exemple:
// deleteElement(filePath, "div", "class", "class-name")
func deleteElement(file, tag, selector, value string) error {

	f, err := os.OpenFile(file, os.O_RDWR, 0660)

	if err != nil {
		return err
	}

	doc, err := goquery.NewDocumentFromReader(f)

	if err != nil {
		return err
	}

	if doc.Find(tag).HasClass(value) {
		doc.Find(tag).Filter("." + value).Remove()

		data, err := goquery.OuterHtml(doc.Selection)

		if err != nil {
			return err
		}

		data = gohtml.Format(data)

		err = f.Truncate(0)

		if err != nil {
			return err
		}
		_, err = f.WriteAt([]byte(data), 0)

		return err
	}
	return nil
}

// append the source content to file
func appendToFile(source, file string) error {

	content, err := ioutil.ReadFile(source)

	if err != nil {
		return err
	}

	f, err := os.OpenFile(file, os.O_RDWR|os.O_CREATE, 0660)
	defer f.Close()

	if err != nil {
		return err
	}

	_, err = f.Write(content)

	return err
}

// allows to append a text to a line
func writeToLine(line, appendText string) string {

	line = strings.TrimRight(line, "\n")
	return line + " " + appendText + "\n"
}

// insert a file into an other file
// exemple:
// insertFile("html", sourceFilePath, destinationFilePath , 10)
// the result will be insert sourceFilePath content in destinationFilePath in line 10
func insertFile(fileType, src, dest string, index int) error {

	f, err := os.OpenFile(dest, os.O_RDWR, 0660)
	defer f.Close()

	if err != nil {
		return err
	}

	scanner := bufio.NewScanner(f)
	lines := []string{}

	for scanner.Scan() {
		lines = append(lines, scanner.Text())
	}
	data, err := ioutil.ReadFile(src)

	lines[index] = writeToLine(lines[index], string(data))

	mergeLines := ""

	for _, l := range lines {
		mergeLines += l
	}

	if fileType == "html" {
		mergeLines = gohtml.Format(mergeLines)
	}

	_, err = f.WriteAt([]byte(mergeLines), 0)
	return err
}

// check if there is a line equal to checkLine variable if not append sec file
func appendFileByLineCheck(src, dest, checkLine string) error {

	f, err := os.OpenFile(dest, os.O_RDWR, 0700)
	defer f.Close()

	if err != nil {
		return err
	}

	scanner := bufio.NewScanner(f)
	buff := ""

	for scanner.Scan() {
		buff += scanner.Text() + "\n"
	}

	if strings.Contains(buff, checkLine) {
		buff = strings.Split(buff, checkLine)[0]
	}
	data, err := ioutil.ReadFile(src)

	buff = buff + string(data)

	err = f.Truncate(0)

	if err != nil {
		return err
	}
	_, err = f.Seek(0, 0)

	if err != nil {
		return err
	}
	_, err = f.Write([]byte(buff))

	return nil
}

// get goquery Document struct from a file path
func getDocFromFile(file string) (*goquery.Document, error) {
	f, err := os.Open(file)
	defer f.Close()

	if err != nil {
		return nil, err
	}

	doc, err := goquery.NewDocumentFromReader(f)

	if err != nil {
		return nil, err
	}

	return doc, nil
}

func updateFiles() {

	/////////////////////////////////////
	// Directory Structure
	/////////////////////////////////////

	// Copy the Golden IMAGE files into the LE 'static' dir
	src := goldenRoot + "images/"
	dest := leImages
	srcFiles, err := ioutil.ReadDir(src)

	if err != nil {
		log.Fatal(err)
	}

	for _, file := range srcFiles {
		srcFile := path.Join(src, file.Name())
		destFile := path.Join(dest, file.Name())
		_, err := placeFile("", srcFile, destFile)

		if err != nil {
			fmt.Println(file.Name(), " Faild to update!")
			log.Fatal(err)
		}
		// fmt.Println(file.Name(), " updated successfully!")
	}

	// Replace the Golden LE CONTENT/EN dir with the WW CONTENT/EN dir only
	srcContent := "golden/content/en"
	destContent := leRoot + "content/en"
	placeDirectory(srcContent, destContent)

	// Replace the Golden LE CONFIG dir with the WW content dir
	srcConfig := "golden/config"
	destConfig := leRoot + "config"
	placeDirectory(srcConfig, destConfig)

	// Delete LE git directory, it doesnt need to be there
	gitDir := leRoot + ".git"
	deleteDirectory(gitDir)

	/////////////////////////////////////
	// Layout Only
	/////////////////////////////////////

	// Replace file favicon
	srcFavicon := "golden/images/favicon.ico"
	destFavicon := leRoot + "static/favicon.ico"
	placeFile("Favicon", srcFavicon, destFavicon)

	//### Head Partial #####
	headHTML := leRoot + "layouts/partials/head.html"
	oldMetaTwitter := "@letsencrypt"
	newMetaTwitter := "@winwisely"
	oldMetaLogo := "images/le-logo-twitter.png"
	newMetaLogo := "wwimages/logo-main.png"
	replaceString(headHTML, oldMetaTwitter, newMetaTwitter)
	replaceString(headHTML, oldMetaLogo, newMetaLogo)

	/////////////////////////////////////
	// Header Partial
	/////////////////////////////////////

	// Replace logo and alt text
	headerHTML := leRoot + "layouts/partials/header.html"
	footerHTML := leRoot + "layouts/partials/footer.html"
	oldLogo := "/images/letsencrypt-logo-horizontal.svg"
	newLogo := "/images/logo-main.png"
	oldAlt := "Let's Encrypt"
	newAlt := "GetCourageNow"
	replaceString(headerHTML, oldLogo, newLogo)
	replaceString(headerHTML, oldAlt, newAlt)

	// Remove hideous foundation link
	deleteElement(headerHTML, "div", "class", "linux-foundation-link")

	// Remove their LE GA link
	replaceString(footerHTML, `<script async src="https://www.googletagmanager.com/gtag/js?id=UA-56433935-1&aip=1"></script>`, "")

	// Replace banner on homepage
	mainCSS := leRoot + "static/css/main.min.css"
	oldBanner := "/images/3.jpg"
	newBanner := "/images/1-dark.jpg"
	replaceString(mainCSS, oldBanner, newBanner)

	// Change banner text
	i18nEN := leRoot + "i18n/en.toml"
	oldHeroTitle := "Let&rsquo;s Encrypt is a <span>free</span>, <span>automated</span>, and <span>open</span> Certificate Authority."
	newHeroTitle := "<span>GetCourageNow</span><br>It&rsquo;s A Numbers Game"
	replaceString(i18nEN, oldHeroTitle, newHeroTitle)

	// Replace contact footer text
	footerHTML = leRoot + "layouts/partials/footer.html"
	oldAddress1 := "1 Letterman Drive, Suite D4700,"
	newAddress1 := "(650) 383 8435 | gary@getcouragenow.org"
	oldAddress2 := "San Francisco,"
	oldAddress3 := "CA"
	oldAddress4 := "94129"
	linuxLink := `{{ i18n "linux_foundation_trademark" }}`
	replaceString(footerHTML, oldAddress1, newAddress1)
	replaceString(footerHTML, oldAddress2, "")
	replaceString(footerHTML, oldAddress3, "")
	replaceString(footerHTML, oldAddress4, "")
	replaceString(footerHTML, linuxLink, "")

	// Replace content in donate footer
	enFile := leRoot + "i18n/en.toml"
	oldDonateBox := "Support a more secure and privacy-respecting Web."
	newDonateBox := "Support us and help scale courage!"
	replaceString(enFile, oldDonateBox, newDonateBox)

	/////////////////////////////////////
	// Homepage Adhoc
	/////////////////////////////////////

	// Append custom home content and css to corresponding files
	customHome := "golden/layouts/home.txt"
	customCSS := "golden/layouts/css.txt"
	customHead := "golden/layouts/google.txt"

	indexPartial := leRoot + "layouts/index.html"
	headPartial := leRoot + "layouts/partials/head.html"
	// basePartial := leRoot + "layouts/_default/baseof.html"
	// blankPartial := leRoot + "layouts/_default/blank.html"
	// postPartial := leRoot + "layouts/post/baseof.html"

	// update resources/website/layouts/index.html file by adding content
	// from golden/layouts/home.txt
	doc, err := getDocFromFile(indexPartial)

	if err != nil {
		log.Fatal(err)
	}

	// Check if there is a div with class name "home-content in index.html"
	if !doc.Find("div").HasClass("home-content") {
		insertFile("html", customHome, indexPartial, 15)
		appendToFile(customCSS, mainCSS)
	}

	// update layouts/partials/head.html file by adding content
	// from "golden/layouts/google.txt"
	doc, err = getDocFromFile(headPartial)

	if err != nil {
		log.Fatal(err)
	}

	// Check if there is a script in head.html
	if !(doc.Find("script").Length() > 0) {
		insertFile("html", customHead, headPartial, 1)
	}

	// Change Button and Link on Banner
	oldButtonLink := "become-a-sponsor"
	newButtonLink := "donate"
	oldButtonText := "home_hero_sponsor"
	newButtonText := "home_hero_donate"

	replaceString(indexPartial, oldButtonLink, newButtonLink)
	replaceString(indexPartial, oldButtonText, newButtonText)

	fmt.Println("Done")

}

// update resources/website content and i18n folders
func updateContentAndI18n() error {

	// remove content folder from resources/website
	err := deleteDirectory(leRoot + "content/")
	if err != nil {
		return err
	}

	// add content folder from golden/ to resources/website
	err = placeDirectory(goldenRoot+"content/", leRoot+"content/")
	if err != nil {
		return err
	}

	// append i18n files to resources/i18n
	src := goldenRoot + "i18n/"
	dest := leRoot + "i18n/"
	srcFiles, err := ioutil.ReadDir(src)

	if err != nil {
		log.Fatal(err)
	}

	for _, file := range srcFiles {
		srcFile := path.Join(src, file.Name())
		destFile := path.Join(dest, file.Name())

		appendFileByLineCheck(srcFile, destFile, "# append")

		if err != nil {
			fmt.Println(file.Name(), " Faild to update!")
			log.Fatal(err)
		}
	}

	return err
}

func main() {
	updateFiles()
	updateContentAndI18n()
}
