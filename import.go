package main

import (
	"bufio"
	"encoding/json"
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
	goldenRoot     = "golden/"
	outputs        = "outputs/hugo/"
	outputsContent = outputs + "content/"
	outputsI18n    = outputs + "/i18n/"
	outputsConfig  = outputs + "/config/"
	leRoot         = "resources/website/"
	leImages       = "resources/website/static/images/"
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
func placeFile(srcFile, destDir, fileName string) (int64, error) {

	f, err := os.Open(srcFile)
	defer f.Close()

	if err != nil {
		fmt.Println(1)
		return 0, err
	}

	os.MkdirAll(destDir, 0700)
	d, err := os.Create(path.Join(destDir, fileName))
	defer d.Close()

	if err != nil {
		fmt.Println(2)
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

	buff = buff + checkLine + "\n" + string(data)

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

	gitDir := leRoot + ".git"
	headerHTML := leRoot + "layouts/partials/header.html"
	mainCSS := leRoot + "static/css/main.min.css"
	customHome := goldenRoot + "layouts/home.txt"
	customCSS := goldenRoot + "layouts/css.txt"
	customHead := goldenRoot + "layouts/google.txt"
	indexPartial := leRoot + "layouts/index.html"
	headPartial := leRoot + "layouts/partials/head.html"

	// Delete LE git directory, it doesnt need to be there
	deleteDirectory(gitDir)
	// Remove hideous foundation link
	deleteElement(headerHTML, "div", "class", "linux-foundation-link")

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
}

func replaceConfig() error {
	destConfig := leRoot + "config"
	return placeDirectory(outputsConfig, destConfig)
}

// Copy the Golden IMAGE files into the LE 'static' dir
func replaceImages() error {
	src := goldenRoot + "images/"
	dest := leImages
	srcFiles, err := ioutil.ReadDir(src)

	if err != nil {
		return err
	}

	for _, file := range srcFiles {
		srcFile := path.Join(src, file.Name())
		_, err := placeFile(srcFile, dest, file.Name())

		if err != nil {
			return err
		}
	}

	// Replace file favicon
	srcFavicon := goldenRoot + "images/favicon.ico"
	destFavicon := leRoot + "static"
	_, err = placeFile(srcFavicon, destFavicon, "favicon.ico")

	return err
}

// Append I18n files from outputs to LE i18n/
func appendI18n() error {

	dest := leRoot + "i18n/"
	srcFiles, err := ioutil.ReadDir(outputsI18n)

	if err != nil {
		return err
	}

	for _, file := range srcFiles {
		srcFile := path.Join(outputsI18n, file.Name())
		destFile := path.Join(dest, file.Name())

		appendFileByLineCheck(srcFile, destFile, "#append")

		if err != nil {
			fmt.Println(file.Name(), " Faild to update!")
			return err
		}
	}
	return nil
}

// Replace Content folders files from outputs to LE content/
func replaceContent() error {

	dirs, err := ioutil.ReadDir(outputsContent)
	if err != nil {
		return err
	}

	for _, dir := range dirs {

		files, err := ioutil.ReadDir(outputsContent + dir.Name())
		if err != nil {
			return err
		}

		for _, file := range files {
			srcFilePath := outputsContent + path.Join(dir.Name(), file.Name())
			destDirPath := leRoot + path.Join("content", dir.Name())

			_, err = placeFile(srcFilePath, destDirPath, file.Name())
			if err != nil {
				return err
			}
		}
	}
	return nil
}

func main() {
	err := replaceImages()
	if err != nil {
		log.Fatal("Could not update images", err)
	}
	fmt.Println("Images directory updated successfully!")

	err = replaceConfig()
	if err != nil {
		log.Fatal("Could not replace config folder", err)
	}
	fmt.Println("Configs directory updated successfully!")

	err = appendI18n()
	if err != nil {
		log.Fatal("Could not append i18n", err)
	}
	fmt.Println("I18n directory updated successfully!")

	err = replaceContent()
	if err != nil {
		log.Fatal("Could not append i18n", err)
	}
	fmt.Println("Contents directory updated successfully!")

	updateFiles()
	fmt.Println("Files updated successfully!")

	err = fixeText()
	if err != nil {
		log.Fatal("Could not append i18n ", err)
	}
	fmt.Println("Text Fixed successfully!")
	fmt.Println("--------------------Done--------------------")
}

type textData struct {
	Old string `json:"old"`
	New string `json:"new"`
}

type errorsModels struct {
	Type     string     `json:"type"`
	FilePath string     `json:"file_path"`
	Errors   []textData `json:"errors"`
}

func fixeText() error {
	file, err := os.Open("fixeText.json")
	defer file.Close()

	if err != nil {
		return err
	}
	errorsM := []errorsModels{}
	err = json.NewDecoder(file).Decode(&errorsM)
	if err != nil {
		return err
	}
	for _, m := range errorsM {

		data, err := ioutil.ReadFile(m.FilePath)
		if err != nil {
			return err
		}
		for _, e := range m.Errors {
			out := strings.ReplaceAll(string(data), e.Old, e.New)

			f, err := os.OpenFile(m.FilePath, os.O_WRONLY|os.O_CREATE, 0700)
			if err != nil {
				return err
			}

			_, err = f.WriteString(out)
			if err != nil {
				return err
			}
			f.Close()
		}
	}
	return nil
}
