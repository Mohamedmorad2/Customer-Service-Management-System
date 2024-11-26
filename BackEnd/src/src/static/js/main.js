

function toggleSidebar() {
    var sidebar = document.querySelector('.sidebar');
    var content = document.getElementById('mainContent');

    sidebar.classList.toggle('open');

    if (sidebar.classList.contains('open')) {
        content.style.width = '85%';
        sidebar.style.left = '0';
    } else {
        content.style.width = '100%';
        sidebar.style.left = '-310px';
    }
}


// Function to automatically close the sidebar based on screen width
function checkScreenWidth() {
    var sidebar = document.querySelector('.sidebar');
    var content = document.getElementById('mainContent');

    if (window.innerWidth >= 180 && window.innerWidth <= 1366) {
        // Close the sidebar if screen width is between 180px and 1366px
        sidebar.classList.remove('open');
        content.style.width = '100%';
        sidebar.style.left = '-310px';
    } else {
        // Keep sidebar open for larger screens
        sidebar.classList.add('open');
        content.style.width = '85%';
        sidebar.style.left = '0';
    }
}

// Run on page load and on window resize
window.addEventListener('load', checkScreenWidth);
window.addEventListener('resize', checkScreenWidth);


document.addEventListener('DOMContentLoaded', function() {
const toggles = document.querySelectorAll('.nav-link.toggle');

toggles.forEach(toggle => {
    toggle.addEventListener('click', function(e) {
        e.preventDefault();
        const submenu = this.nextElementSibling;

          // Close all submenus
        document.querySelectorAll('.submenu').forEach(sub => {
            if (sub !== submenu) {
                sub.style.display = 'none';
            }
        });

          // Toggle the clicked submenu
        if (submenu.style.display == 'block') {
            submenu.style.display = 'none';
        } else {
            submenu.style.display = 'block';
        }
    });
});
});

function sortTable(n) {
    const table = document.getElementById("Table");
    const rows = Array.from(table.getElementsByTagName("TR")).slice(1);
    const isAscending = table.querySelector(`th:nth-child(${n + 1})`).classList.toggle("asc");
    
    rows.sort((a, b) => {
        const aText = a.getElementsByTagName("TD")[n].innerText;
        const bText = b.getElementsByTagName("TD")[n].innerText;
        
        if (n === 2) {
            return isAscending
                ? new Date(aText) - new Date(bText)
                : new Date(bText) - new Date(aText);
        }
        
        return isAscending
            ? aText.localeCompare(bText, undefined, { numeric: true })
            : bText.localeCompare(aText, undefined, { numeric: true });
    });
    
    rows.forEach(row => table.querySelector("tbody").appendChild(row));
}


$(document).ready(function() {
    var table = $('#example').DataTable({
        lengthMenu: [25,50, 100, 150, 250],
        dom: '<"top"lf>rt<"bottom"ip><"clear">', 
        initComplete: function() {
            $('#example_length').appendTo('#custom-controls');
            $('#example_filter').detach().prependTo('#example_wrapper .top');
        }
    });
});

