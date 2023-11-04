const tablesContainer = document.getElementById("tables-container");
        const provinceDropdown = document.getElementById("province-dropdown");
        const cubeTypeDropdown = document.getElementById("wcaevent-dropdown");
        let parsedData = [];
        let currentSortColumn = `avg${cubeTypeDropdown.value}`; // 'avg333' or 'avg222'
	let currentAvatarPopup = null;


	function decodeSingleMBLD(value) {
	  const difference = 99 - parseInt(value.substring(0, 2));
	  const timeInSeconds = parseInt(value.substring(2, 7));
	  const missed = parseInt(value.substring(7, 9));
	  const solved = difference + missed;
	  const attempted = solved + missed;
	  return `${solved}/${attempted} ${Math.floor(timeInSeconds / 60).toString().padStart(2, '0')}:${(timeInSeconds % 60).toString().padStart(2, '0')}`;
	}
	    
        function parseTable(tableHTML) {
            const parser = new DOMParser();
            const doc = parser.parseFromString(tableHTML, 'text/html');
            const table = doc.querySelector('table');
            const rows = table.querySelectorAll('tbody tr');
            const parsedData = [];
            rows.forEach((row, index) => {
                const columns = row.querySelectorAll('td');
                if (columns.length >= 2) {
                    const id = columns[0].textContent;
                    const avg333 = columns[1].textContent;
                    const province = columns[2] ? columns[2].textContent : 'BC';
                    const single333 = columns[3].textContent;
                    const photo = columns[4].textContent;
                    const avg222 = columns[5].textContent;
                    const single222 = columns[6].textContent;
                    const avg444 = columns[7].textContent;
                    const single444 = columns[8].textContent;
                    const avg555 = columns[9].textContent;
                    const single555 = columns[10].textContent;
                    const avg666 = columns[11].textContent;
                    const single666 = columns[12].textContent;
                    const avg777 = columns[13].textContent;
		    const single777 = columns[14].textContent;
		    const avg3bld = columns[15].textContent;
                    const single3bld = columns[16].textContent;
                    const avgfmc = columns[17].textContent;
                    const singlefmc = columns[18].textContent;
                    const avgoh = columns[19].textContent;
                    const singleoh = columns[20].textContent;
		    const avgclock = columns[21].textContent;
                    const singleclock = columns[22].textContent;
                    const avgmega = columns[23].textContent;
                    const singlemega = columns[24].textContent;
                    const avgpyra = columns[25].textContent;
                    const singlepyra = columns[26].textContent;
                    const avgskewb = columns[27].textContent;
                    const singleskewb = columns[28].textContent;
                    const avgsq1 = columns[29].textContent;
                    const singlesq1 = columns[30].textContent;
                    const avg4bld = columns[31].textContent;
                    const single4bld = columns[32].textContent;
                    const avg5bld = columns[33].textContent;
                    const single5bld = columns[34].textContent;
                    const avgmbld = columns[35].textContent;
                    const singlembld = columns[36].textContent;
		    const decodedSingleMBLD = decodeSingleMBLD(singlembld);
                    const name = columns[37].textContent;
                    parsedData.push({
                        id,
                        avg333,
                        province,
                        single333,
                        photo,
                        avg222,
                        single222,
                        avg444,
                        single444,
                        avg555,
                        single555,
                        avg666,
                        single666,
                        avg777,
                        single777,
			avg3bld,
                        single3bld,
                        avgfmc,
                        singlefmc,
                        avgoh,
                        singleoh,
			avgclock,
                        singleclock,
                        avgmega,
                        singlemega,
                        avgpyra,
                        singlepyra,
                        avgskewb,
                        singleskewb,
                        avgsq1,
                        singlesq1,
                        avg4bld,
                        single4bld,
                        avg5bld,
                        single5bld,
                        avgmbld,
                        singlembld,
                        name,
                    });
                }
            });
            return parsedData;
        }
	
        function parseTimeToNumber(timeValue) {
            if (timeValue.includes(':')) {
                const [minutes, seconds] = timeValue.split(':');
                return parseFloat(minutes) * 60 + parseFloat(seconds);
            }
            return parseFloat(timeValue);
        }

        function createTable(rows, cubeType) {
			
	    const table = document.createElement("table");
	    table.border = "1";
	    table.className = "dataframe table table-bordered table-hover";
	    table.innerHTML = `
	        <thead>
	            <tr>
	                <th>Rank</th>
	                <th>Name</th>
		 	<th class="sortable-header" data-sort-column="single${cubeType}">PR Single</th>
	                <th class="sortable-header" data-sort-column="${currentSortColumn}">PR Avg</th>
	            </tr>
	        </thead>
	        <tbody></tbody>
	    `;
	
	    rows = rows.filter(row => !isNaN(parseTimeToNumber(row[`single${cubeType}`])));   // Fix this line

	    // Sorting logic
	    rows.sort((a, b) => {
	        const aSingle = parseTimeToNumber(a[`single${cubeType}`]);
	        const bSingle = parseTimeToNumber(b[`single${cubeType}`]);
        
        // For 'bld' events, sort by single.
        if (['3bld', '4bld', '5bld'].includes(cubeTypeDropdown.value)) {
            return aSingle - bSingle;
        }

        const aAvg = parseTimeToNumber(a[currentSortColumn]);
        const bAvg = parseTimeToNumber(b[currentSortColumn]);

        // For all other events
        if (!isNaN(aAvg) && !isNaN(bAvg)) {
            return aAvg - bAvg;
        } else if (!isNaN(aAvg)) {
            return -1;
        } else if (!isNaN(bAvg)) {
            return 1;
        } else {
            return aSingle - bSingle;
        }
    });

    for (let i = 0; i < rows.length; i++) {
        const row = rows[i];
        const tr = document.createElement("tr");
        const prAvg = row[currentSortColumn] !== 'NaN' ? row[currentSortColumn] : '';
        const prSingle = (cubeType === 'mbld' ? decodeSingleMBLD(row[`single${cubeType}`]) : row[`single${cubeType}`]) !== 'NaN' ? (cubeType === 'mbld' ? decodeSingleMBLD(row[`single${cubeType}`]) : row[`single${cubeType}`]) : '';
		
		
        tr.innerHTML = `
            <td>${i + 1}</td>
            <td class="name-cell">
                <a href="https://worldcubeassociation.org/persons/${row.id}" target="_blank">
                    <img src="${row.photo}" alt="${row.name}" width="60" style="margin-right: 10px">
                    ${row.name}
                </a>
            </td>
            <td>${prSingle}</td>
            <td>${prAvg}</td>
        `;

        // Add a mouseover event to show the avatar pop-up with a delay
        let avatarPopupTimer;
        const avatarImage = tr.querySelector("img");

        if (row.photo !== "https://www.worldcubeassociation.org/assets/missing_avatar_thumb-d77f478a307a91a9d4a083ad197012a391d5410f6dd26cb0b0e3118a5de71438.png") {
            avatarImage.addEventListener("mouseover", (event) => {
                avatarPopupTimer = setTimeout(() => {
                    showAvatarPopup(row.photo, row.name, event);
                }, 750); // 750ms (0.75 seconds) delay
            });

            // Add a mouseout event to hide the pop-up when the cursor leaves the image
            avatarImage.addEventListener("mouseout", () => {
                clearTimeout(avatarPopupTimer);
                hideAvatarPopup();
            });
        }

        table.querySelector("tbody").appendChild(tr);
    }

    return table;
}

	    
        function showTable(province, cubeType) {
	    hideAvatarPopup();
	    tablesContainer.innerHTML = "";
	    currentSortColumn = `avg${cubeType}`;
	    const filteredRows = parsedData.filter(row => row.province === province);
	    tablesContainer.appendChild(createTable(filteredRows, cubeType));
	}

	/* function onHeaderClick(event) { 
            const clickedColumn = event.target.getAttribute('data-sort-column');

            if (clickedColumn) {
                currentSortColumn = clickedColumn;
                showTable(provinceDropdown.value, cubeTypeDropdown.value);
            }
        } */

	function toggleDarkMode() {
	    const body = document.body;
	    body.classList.toggle("dark-mode");
	
	    // Save the dark mode preference to localStorage
	    if (body.classList.contains("dark-mode")) {
	        localStorage.setItem("dark-mode", "enabled");
	    } else {
	        localStorage.setItem("dark-mode", "disabled");
	    }
	}

	function showAvatarPopup(imageUrl, name, event) {
	    // Close the existing avatar popup
	    hideAvatarPopup();
	
	    // Create the avatar pop-up element
	    const avatarPopup = document.createElement("div");
	    avatarPopup.className = "avatar-popup";
	
	    // Create the image element inside the pop-up
	    const avatarImage = document.createElement("img");
	    avatarImage.src = imageUrl;
	    avatarImage.alt = name;
	
	    // Append the image to the pop-up
	    avatarPopup.appendChild(avatarImage);
	
	    // Calculate the position based on the cursor's position
	    const popupX = event.clientX;
	    const popupY = event.clientY;
	
	    // Set the position of the pop-up
	    avatarPopup.style.left = popupX + "px";
	    avatarPopup.style.top = popupY + "px";
	
	    // Append the pop-up to the body
	    document.body.appendChild(avatarPopup);
	
	    // Display the pop-up
	    avatarPopup.style.display = "block";
	
	    // Set the current open avatar popup
	    currentAvatarPopup = avatarPopup;
	
	    // Make the popup draggable
	    let isDragging = false;
	    let offsetX, offsetY;
	
	    avatarPopup.addEventListener("mousedown", (e) => {
	        isDragging = true;
	        offsetX = e.clientX - avatarPopup.getBoundingClientRect().left;
	        offsetY = e.clientY - avatarPopup.getBoundingClientRect().top;
	    });
	
	    document.addEventListener("mousemove", (e) => {
	        if (isDragging) {
	            const newX = e.clientX - offsetX;
	            const newY = e.clientY - offsetY;
	            avatarPopup.style.left = newX + "px";
	            avatarPopup.style.top = newY + "px";
	        }
	    });
	
	    document.addEventListener("mouseup", () => {
	        isDragging = false;
	    });
	
	    // Add event listeners to prevent the popup from closing
	    avatarPopup.addEventListener("mouseover", (event) => {
	        event.stopPropagation();
	    });
	
	    // Add an event listener to close the pop-up when clicking outside of it
	    avatarPopup.addEventListener("click", hideAvatarPopup);
	
	    // Add event listener to open the link when clicking on the avatar
	    avatarImage.addEventListener("click", (event) => {
	        event.stopPropagation(); // Prevent the click from closing the popup
	        window.open(imageUrl, "_blank");
	    });
	}
	
	function hideAvatarPopup() {
	    if (currentAvatarPopup) {
	        currentAvatarPopup.style.display = "none";
	        currentAvatarPopup.remove();
	        currentAvatarPopup = null;
		
	            // Remove the event listener to close the pop-up when clicking outside
	            document.removeEventListener("click", hideAvatarPopup);
	        }
	    }
	
		if (localStorage.getItem("dark-mode") === "enabled") {
		    document.body.classList.add("dark-mode");
		}
			    
	        provinceDropdown.addEventListener("change", (event) => {
	            const selectedProvince = event.target.value;
	            showTable(selectedProvince, cubeTypeDropdown.value);
	        });
	
	        cubeTypeDropdown.addEventListener("change", (event) => {
	            const selectedCubeType = event.target.value;
	            showTable(provinceDropdown.value, selectedCubeType);
	        });
	
	        fetch(`final_sorted_RESULTS.html`)
	            .then(response => response.text())
	            .then(tableHTML => {
	                parsedData = parseTable(tableHTML);
	                showTable(provinceDropdown.value, cubeTypeDropdown.value);
	            })
	            .catch(error => console.error(error));
	
		// avatarImage.addEventListener("mouseout", () => {
		//     clearTimeout(avatarPopupTimer);
		//     hideAvatarPopup();
		// });
			    
	        document.addEventListener('click', (event) => {
	            if (event.target.classList.contains('sortable-header')) {
	                onHeaderClick(event);
	            }
	        });

// Define your function to be called when an option is selected
function handleSelectionChange() {
	var cubeIconLink = document.getElementById("cubeIcon");
	var selectElement = document.getElementById("wcaevent-dropdown");
	var selectedValue = selectElement.value;
  
	// You can perform actions based on the selected value here
	console.log("Selected value: " + selectedValue);
	switch (selectedValue) {
		case '222':
			cubeIconLink.href = "icons/222.png";
			break;
		case '333':
			cubeIconLink.href = "icons/333.png";
			break;
		case '444':
			cubeIconLink.href = "icons/444.png";
			break;
		case '555':
			cubeIconLink.href = "icons/555.png";
			break;
		case '666':
			cubeIconLink.href = "icons/666.png";
			break;
		case '777':
			cubeIconLink.href = "icons/777.png";
			break;
		case '3bld':
			cubeIconLink.href = "icons/333bf.png";
			break;
		case 'fmc':
			cubeIconLink.href = "icons/333fm.png";
			break;
		case 'oh':
			cubeIconLink.href = "icons/333oh.png";
			break;
		case 'clock':
			cubeIconLink.href = "icons/clock.png";
			break;
		case 'mega':
			cubeIconLink.href = "icons/minx.png";
			break;
		case 'pyra':
			cubeIconLink.href = "icons/pyram.png";
			break;
		case 'skewb':
			cubeIconLink.href = "icons/skewb.png";
			break;
		case 'sq1':
			cubeIconLink.href = "icons/sq1.png";
			break;
		case '4bld':
			cubeIconLink.href = "icons/444bf.png";
			break;
		case '5bld':
			cubeIconLink.href = "icons/555bf.png";
			break;
		case 'mbld':
			cubeIconLink.href = "icons/333mbf.png";
			break;
	}
}

// Add an event listener to the select element
var selectElement = document.getElementById("wcaevent-dropdown");
selectElement.addEventListener("change", handleSelectionChange);
