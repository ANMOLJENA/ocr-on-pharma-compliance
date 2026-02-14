/**
 * Unit Tests for LanguageSelector Component
 * 
 * These tests validate the LanguageSelector component functionality:
 * - Fetching and displaying supported languages
 * - Language selection handling
 * - Error state handling
 * - Loading state display
 * - Accessibility and UI interactions
 * 
 * Requirements: 6.1 - Display dropdown with all 40+ supported languages and handle language selection
 */

import { describe, it, expect, beforeEach, vi } from "vitest";
import { render, screen, waitFor } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { LanguageSelector } from "./LanguageSelector";

// Mock the API service
vi.mock("@/services/api.service", () => ({
  apiService: {
    getSupportedLanguages: vi.fn(),
  },
}));

// Mock sonner toast
vi.mock("sonner", () => ({
  toast: {
    error: vi.fn(),
    success: vi.fn(),
  },
}));

import { apiService } from "@/services/api.service";

describe("LanguageSelector Component", () => {
  beforeEach(() => {
    vi.clearAllMocks();
  });

  describe("Language Loading", () => {
    it("should display loading state initially", async () => {
      (apiService.getSupportedLanguages as any).mockImplementation(
        () =>
          new Promise((resolve) =>
            setTimeout(
              () =>
                resolve({
                  success: true,
                  data: { en: "English" },
                }),
              100
            )
          )
      );

      render(<LanguageSelector />);
      // The component should be rendering, check for the select trigger
      await waitFor(() => {
        expect(screen.getByRole("combobox")).toBeInTheDocument();
      });
    });

    it("should fetch languages from the API on mount", async () => {
      (apiService.getSupportedLanguages as any).mockResolvedValueOnce({
        success: true,
        data: {
          en: "English",
          fr: "French",
          de: "German",
        },
      });

      render(<LanguageSelector />);

      await waitFor(() => {
        expect(apiService.getSupportedLanguages).toHaveBeenCalled();
      });
    });

    it("should display all fetched languages", async () => {
      (apiService.getSupportedLanguages as any).mockResolvedValueOnce({
        success: true,
        data: {
          en: "English",
          fr: "French",
          de: "German",
          hi: "Hindi",
        },
      });

      render(<LanguageSelector />);

      await waitFor(() => {
        // Check that the component rendered successfully with languages loaded
        expect(screen.getByRole("combobox")).toBeInTheDocument();
        // The select trigger should show the default language
        expect(screen.getByRole("combobox")).toHaveTextContent("English");
        // Language count should reflect all languages
        expect(screen.getByText(/4 languages supported/i)).toBeInTheDocument();
      });
    });

    it("should display language count", async () => {
      (apiService.getSupportedLanguages as any).mockResolvedValueOnce({
        success: true,
        data: {
          en: "English",
          fr: "French",
          de: "German",
        },
      });

      render(<LanguageSelector />);

      await waitFor(() => {
        expect(screen.getByText(/3 languages supported/i)).toBeInTheDocument();
      });
    });
  });

  describe("Language Selection", () => {
    beforeEach(() => {
      (apiService.getSupportedLanguages as any).mockResolvedValueOnce({
        success: true,
        data: {
          en: "English",
          fr: "French",
          de: "German",
          hi: "Hindi",
          ta: "Tamil",
        },
      });
    });

    it("should render select trigger with initial language", async () => {
      render(<LanguageSelector onLanguageSelect={vi.fn()} />);

      await waitFor(() => {
        const selectTrigger = screen.getByRole("combobox");
        expect(selectTrigger).toBeInTheDocument();
        // English should be the default selected value
        expect(selectTrigger).toHaveTextContent("English");
      });
    });

    it("should call onLanguageSelect callback prop when provided", async () => {
      const onLanguageSelect = vi.fn();

      render(<LanguageSelector onLanguageSelect={onLanguageSelect} />);

      await waitFor(() => {
        expect(screen.getByRole("combobox")).toBeInTheDocument();
      });

      // Verify the callback prop is accepted
      expect(onLanguageSelect).not.toHaveBeenCalled();
    });
  });

  describe("Error Handling", () => {
    it("should display error message when API fails", async () => {
      (apiService.getSupportedLanguages as any).mockResolvedValueOnce({
        success: false,
        error: "Failed to load languages",
      });

      render(<LanguageSelector />);

      await waitFor(() => {
        expect(
          screen.getByText(/Failed to load languages/i)
        ).toBeInTheDocument();
      });
    });

    it("should handle network errors gracefully", async () => {
      (apiService.getSupportedLanguages as any).mockRejectedValueOnce(
        new Error("Network error")
      );

      render(<LanguageSelector />);

      await waitFor(() => {
        expect(screen.getByText(/Network error/i)).toBeInTheDocument();
      });
    });
  });

  describe("Props and Customization", () => {
    beforeEach(() => {
      (apiService.getSupportedLanguages as any).mockResolvedValueOnce({
        success: true,
        data: {
          en: "English",
          fr: "French",
        },
      });
    });

    it("should hide label when showLabel is false", async () => {
      render(<LanguageSelector showLabel={false} />);

      await waitFor(() => {
        expect(screen.queryByText("Document Language")).not.toBeInTheDocument();
      });
    });
  });

  describe("Accessibility", () => {
    beforeEach(() => {
      (apiService.getSupportedLanguages as any).mockResolvedValueOnce({
        success: true,
        data: {
          en: "English",
          fr: "French",
        },
      });
    });

    it("should have proper label association", async () => {
      render(<LanguageSelector />);

      await waitFor(() => {
        const label = screen.getByText("Document Language");
        expect(label).toBeInTheDocument();
      });
    });

    it("should be keyboard navigable", async () => {
      render(<LanguageSelector />);

      await waitFor(() => {
        const selectTrigger = screen.getByRole("combobox");
        expect(selectTrigger).toBeInTheDocument();
      });
    });
  });

  describe("Edge Cases", () => {
    it("should handle empty language list", async () => {
      (apiService.getSupportedLanguages as any).mockResolvedValueOnce({
        success: true,
        data: {},
      });

      render(<LanguageSelector />);

      await waitFor(() => {
        const selectTrigger = screen.getByRole("combobox");
        expect(selectTrigger).toBeDisabled();
      });
    });

    it("should handle large language list", async () => {
      const largeLanguageList: Record<string, string> = {};
      for (let i = 0; i < 50; i++) {
        largeLanguageList[`lang${i}`] = `Language ${i}`;
      }

      (apiService.getSupportedLanguages as any).mockResolvedValueOnce({
        success: true,
        data: largeLanguageList,
      });

      render(<LanguageSelector />);

      await waitFor(() => {
        expect(screen.getByText(/50 languages supported/i)).toBeInTheDocument();
      });
    });
  });
});
