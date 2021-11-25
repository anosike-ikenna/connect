class FileHandler {
    /**
     * 
     * @param {string} fileElQuery the css query to get the file element
     * @param {string} targetElQuery the css query of the element where the name of the file should be displayed (if any)
     * @param {Array} fileTypes an array containing file types that should be supported (if any)
     */
    constructor(fileElQuery, targetElQuery, fileTypes) {
        this._fileElement = fileElQuery;
        this._targetElement = targetElQuery;
        this.files = [];
        this.input = null;
        this._fileTypes = fileTypes;
    }

    processFile() {
        this.input = document.querySelector(this._fileElement);
        if (this.input) {
            this.input.addEventListener("change", () => {
                if (this.input.files.length > 0) {
                    this.files = this.input.files;
                    if (this.validateFile()) {
                        if (this._targetElement) {
                            this.display();
                        }
                    }
                }
            });
        }
    }

    display() {
        let displayElement = document.querySelector(this._targetElement);
        let fileNames = [];
        for (let file of Array.from(this.files)) {
            let reader = new FileReader();
            reader.addEventListener("load", () => {
                displayElement.setAttribute("href", reader.result);
            });
            reader.readAsDataURL(file);
            fileNames.push(file.name);
        }
        displayElement.textContent = fileNames.join(", ");
    }

    validateFile() {
        if (this._fileTypes) {
            for (let file of this.files) {
                if (this._fileTypes.indexOf(file.type) == -1) {
                    alert(`${file.name} is of an unsupported format (${file.type})`);
                    this.input.value = "";
                    return false;
                }
            }
        }
        return true;
    }

}