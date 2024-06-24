const puppeteer = require('puppeteer');

let lastMousePosition = { x: 0, y: 0 };

async function main() {
    const browser = await puppeteer.launch({ headless: false });
    const page = await browser.newPage();
    await page.goto('http://127.0.0.1:5000');

    await injectDotFunctions(page);

    lastMousePosition = { x: 100, y: 100 }; // Starting point

    const username = 'admin';
    let passwordAttempt = 1;
    let success = false;

    while (passwordAttempt <= 100 && !success) {
        success = await loginProcess(page, username, String(passwordAttempt));
        if (!success) {
            // Reset the page for the next attempt
            await page.goto('http://127.0.0.1:5000');
            await page.waitForTimeout(10); // Wait for page reload
        }
        passwordAttempt++;
        await page.waitForTimeout(10);
    }

    if (success) {
        console.log('Login successful. Script is now waiting. Close the browser window manually to exit.');
        await page.evaluate(() => window.removeAllDots());
        await page.waitForTimeout(10); // Wait for 10 minutes
    } else {
        console.log('Failed to login after 100 attempts.');
    }

    await browser.close();
}

async function injectDotFunctions(page) {
    await page.evaluate(() => {
        window.createDot = (x, y) => {
            const dot = document.createElement('div');
            dot.style.width = '5px';
            dot.style.height = '5px';
            dot.style.backgroundColor = 'red';
            dot.style.position = 'absolute';
            dot.style.borderRadius = '50%';
            dot.style.left = `${x}px`;
            dot.style.top = `${y}px`;
            document.body.appendChild(dot);
        };

        window.removeAllDots = () => {
            document.querySelectorAll('div').forEach(el => {
                if (el.style.position === 'absolute' && el.style.backgroundColor === 'red') {
                    el.remove();
                }
            });
        };
    });
}

async function loginProcess(page, username, password) {
    try {
        await injectDotFunctions(page);
        await moveAndType(page, '#loginEmail', username);
        await moveAndType(page, '#loginPassword', password);
        await moveAndType(page, '#robotCheck', 'I am not a robot');
        await moveToElement(page, "input[type='submit']");
        await page.click("input[type='submit']");

        await page.waitForNavigation();
        await page.waitForSelector('#message');
        const message = await page.$eval('#message', el => el.innerText);
        return message.includes('Login successful!');
    } catch (e) {
        console.error(`An error occurred during login: ${e}`);
        return false;
    }
}

async function moveAndType(page, selector, text) {
    await moveToElement(page, selector);
    const element = await page.$(selector);
    await element.type(text);
}

async function moveToElement(page, selector) {
    const element = await page.$(selector);
    const boundingBox = await element.boundingBox();
    const targetX = boundingBox.x + boundingBox.width / 2;
    const targetY = boundingBox.y + boundingBox.height / 2;
    await humanLikeMouseMove(page, targetX, targetY);
}

async function humanLikeMouseMove(page, targetX, targetY) {
    const mouse = page.mouse;
    const steps = 15;

    for (let i = 1; i <= steps; i++) {
        const progress = i / steps;
        const x = getBezierPoint(lastMousePosition.x, targetX, progress) + randomDeviation(10);
        const y = getBezierPoint(lastMousePosition.y, targetY, progress) + randomDeviation(10);

        await mouse.move(x, y);
        await page.evaluate((x, y) => window.createDot(x, y), x, y);
        await page.waitForTimeout(randomInterval(10, 30));
    }

    lastMousePosition = { x: targetX, y: targetY };
}

function getBezierPoint(start, end, t) {
    return (1 - t) * start + t * end;
}

function randomDeviation(maxDeviation = 5) {
    return Math.random() * maxDeviation - maxDeviation / 2;
}

function randomInterval(min = 10, max = 30) {
    return Math.floor(Math.random() * (max - min + 1) + min);
}

main();
