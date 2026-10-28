import {test, expect} from '@playwright/test'
import {mkdir, readFile} from 'node:fs/promises'
import path from 'node:path'

const screenshots = path.resolve('artifacts', 'browser-screenshots')

test('real dashboard renders and exports actual physics scenarios', async ({page}) => {
  await mkdir(screenshots, {recursive: true})
  await page.goto('/')
  await expect(page.getByRole('heading', {name: /See the mission/i})).toBeVisible()
  await expect(page.getByText('ISS / 25544')).toBeVisible()
  await page.screenshot({path:path.join(screenshots,'01-mission-overview.png'),fullPage:true})

  await page.getByRole('button', {name:'Scenario Comparison'}).click()
  await expect(page.getByRole('heading', {name:'Scenario Comparison Lab'})).toBeVisible()
  await expect(page.locator('.scenario-stat')).toHaveCount(4)
  await page.locator('.scenario-layout select').selectOption('density_multiplier')
  await page.getByLabel('Comma-separated scenario values').fill('0.5, 1, 2')
  await page.getByRole('button', {name:/Compare simulated trajectories/}).click()
  await expect(page.locator('.scenario-stat')).toHaveCount(3)
  await expect(page.locator('.scenario-stat').first()).toContainText('0.5')
  await expect(page.locator('.recharts-line')).toHaveCount(3)
  await page.screenshot({path:path.join(screenshots,'02-rocket-comparison.png'),fullPage:true})

  const transfer=page.waitForEvent('download')
  await page.getByRole('button', {name:'Export table CSV'}).click()
  const download=await transfer
  expect(download.suggestedFilename()).toContain('rocket-comparison-demo.csv')
  const csv=await readFile(await download.path(),'utf8')
  expect(csv).toContain('apogee_km')
  expect(csv.split('\n').filter(Boolean)).toHaveLength(4)

  await page.getByRole('button', {name:'Rocket Lab'}).click()
  await expect(page.getByRole('heading', {name:'Rocket Trajectory Laboratory'})).toBeVisible()
  await page.screenshot({path:path.join(screenshots,'03-rocket-lab.png'),fullPage:true})
})

test('invalid comparison values show accessible client validation', async ({page}) => {
  await page.goto('/')
  await page.getByRole('button',{name:'Scenario Comparison'}).click()
  await expect(page.locator('.scenario-stat')).toHaveCount(4)
  await page.getByLabel('Comma-separated scenario values').fill('30000, 30000')
  await page.getByRole('button',{name:/Compare simulated trajectories/}).click()
  await expect(page.getByRole('alert')).toContainText('unique numeric scenario values')
})
