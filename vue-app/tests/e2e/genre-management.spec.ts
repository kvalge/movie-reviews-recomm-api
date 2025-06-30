import { test, expect } from '@playwright/test'

test.describe('Genre Management E2E Tests', () => {
  test.beforeEach(async ({ page }) => {
    page.on('request', request => console.log(`>> ${request.method()} ${request.url()}`))
    page.on('response', response => console.log(`<< ${response.status()} ${response.url()}`))

    await page.goto('/')

    await page.evaluate(() => {
      localStorage.setItem('token', 'mock-jwt-token')
      localStorage.setItem('user', JSON.stringify({
        id: 1,
        username: 'admin',
        email: 'admin@example.com'
      }))
    })

    await page.goto('/manage-movie-data')

    await expect(page.locator('h1')).toHaveText('Manage Movie Data', { timeout: 10000 })
  })

  test('should navigate to genre management page', async ({ page }) => {
    await expect(page.locator('h1')).toHaveText('Manage Movie Data')
  })

  test('should display genres component', async ({ page }) => {
    // Check if the Genre component is rendered
    await expect(page.locator('.container')).toBeVisible()
  })

  test('should show add genre button', async ({ page }) => {
    await expect(page.locator('[data-test="add-genre-button"]')).toBeVisible()
    await expect(page.locator('[data-test="add-genre-button"]')).toContainText('Add New Genre')
  })

  test('should display existing genres with edit and delete buttons', async ({ page }) => {
    await expect(page.locator('[data-test="edit-genre-button"]').first()).toBeVisible()
    await expect(page.locator('[data-test="delete-genre-button"]').first()).toBeVisible()

    const editButtonCount = await page.locator('[data-test="edit-genre-button"]').count()
    const deleteButtonCount = await page.locator('[data-test="delete-genre-button"]').count()
    
    expect(editButtonCount).toBeGreaterThan(0)
    expect(deleteButtonCount).toBeGreaterThan(0)
    expect(editButtonCount).toBe(deleteButtonCount) // Should be equal
  })

  test('should show save genre button', async ({ page }) => {
    await expect(page.locator('[data-test="save-genre-button"]')).toBeVisible()
    await expect(page.locator('[data-test="save-genre-button"]')).toContainText('Save Genre')
  })

  test('should count multiple genre items', async ({ page }) => {
    const editButtons = page.locator('[data-test="edit-genre-button"]')
    const buttonCount = await editButtons.count()
    expect(buttonCount).toBeGreaterThan(0)

    for (let i = 0; i < buttonCount; i++) {
      await expect(editButtons.nth(i)).toContainText('Edit')
    }
  })
}) 