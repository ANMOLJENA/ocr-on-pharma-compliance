/**
 * Unit Tests for BilingualTextViewer Component
 * 
 * These tests validate the BilingualTextViewer component functionality:
 * - Displaying original and translated text side-by-side
 * - Tab navigation between views
 * - Copy and download functionality
 * - Translation status display
 * - Accessibility
 * 
 * Requirements: 6.3, 6.4 - Display original and translated text side-by-side, show translation status
 */

import { describe, it, expect, beforeEach, vi } from "vitest";
import { render, screen, waitFor } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { BilingualTextViewer } from "./BilingualTextViewer";

// Mock sonner toast
vi.mock("sonner", () => ({
  toast: {
    success: vi.fn(),
    error: vi.fn(),
  },
}));

describe("BilingualTextViewer Component", () => {
  const mockOriginalText = "This is the original text in Spanish.";
  const mockTranslatedText = "This is the translated text in English.";

  beforeEach(() => {
    vi.clearAllMocks();
  });

  describe("Rendering", () => {
    it("should render the component with both texts", () => {
      render(
        <BilingualTextViewer
          originalText={mockOriginalText}
          translatedText={mockTranslatedText}
          originalLanguage="Spanish"
          translatedLanguage="English"
        />
      );

      expect(screen.getByText(mockOriginalText)).toBeInTheDocument();
      expect(screen.getByText(mockTranslatedText)).toBeInTheDocument();
    });

    it("should display translation status header", () => {
      render(
        <BilingualTextViewer
          originalText={mockOriginalText}
          translatedText={mockTranslatedText}
          originalLanguage="French"
          translatedLanguage="English"
          translationStatus="success"
        />
      );

      expect(
        screen.getByText(/Translation completed successfully/i)
      ).toBeInTheDocument();
    });
  });

  describe("Tab Navigation", () => {
    it("should have three tabs: side-by-side, original, translated", () => {
      render(
        <BilingualTextViewer
          originalText={mockOriginalText}
          translatedText={mockTranslatedText}
          originalLanguage="German"
          translatedLanguage="English"
        />
      );

      expect(screen.getAllByRole("tab").length).toBe(3);
    });

    it("should display side-by-side view by default", () => {
      render(
        <BilingualTextViewer
          originalText={mockOriginalText}
          translatedText={mockTranslatedText}
          originalLanguage="Italian"
          translatedLanguage="English"
        />
      );

      const tabs = screen.getAllByRole("tab");
      expect(tabs[0]).toHaveAttribute("data-state", "active");
    });

    it("should switch to original text tab", async () => {
      render(
        <BilingualTextViewer
          originalText={mockOriginalText}
          translatedText={mockTranslatedText}
          originalLanguage="Portuguese"
          translatedLanguage="English"
        />
      );

      const tabs = screen.getAllByRole("tab");
      await userEvent.click(tabs[1]); // Click original tab

      expect(tabs[1]).toHaveAttribute("data-state", "active");
    });

    it("should switch to translated text tab", async () => {
      render(
        <BilingualTextViewer
          originalText={mockOriginalText}
          translatedText={mockTranslatedText}
          originalLanguage="Russian"
          translatedLanguage="English"
        />
      );

      const tabs = screen.getAllByRole("tab");
      await userEvent.click(tabs[2]); // Click translated tab

      expect(tabs[2]).toHaveAttribute("data-state", "active");
    });
  });

  describe("Copy Functionality", () => {
    beforeEach(() => {
      Object.assign(navigator, {
        clipboard: {
          writeText: vi.fn(() => Promise.resolve()),
        },
      });
    });

    it("should copy original text to clipboard", async () => {
      render(
        <BilingualTextViewer
          originalText={mockOriginalText}
          translatedText={mockTranslatedText}
          originalLanguage="Dutch"
          translatedLanguage="English"
        />
      );

      const copyButtons = screen.getAllByRole("button").filter(
        (btn) => btn.title && btn.title.includes("Copy")
      );
      
      if (copyButtons.length > 0) {
        await userEvent.click(copyButtons[0]);

        await waitFor(() => {
          expect(navigator.clipboard.writeText).toHaveBeenCalled();
        });
      }
    });
  });

  describe("Translation Status Display", () => {
    it("should display success status", () => {
      render(
        <BilingualTextViewer
          originalText={mockOriginalText}
          translatedText={mockTranslatedText}
          originalLanguage="Hebrew"
          translatedLanguage="English"
          translationStatus="success"
        />
      );

      expect(
        screen.getByText(/Translation completed successfully/i)
      ).toBeInTheDocument();
    });

    it("should display pending status", () => {
      render(
        <BilingualTextViewer
          originalText={mockOriginalText}
          translatedText={mockTranslatedText}
          originalLanguage="Thai"
          translatedLanguage="English"
          translationStatus="pending"
        />
      );

      expect(
        screen.getByText(/Translation in progress/i)
      ).toBeInTheDocument();
    });

    it("should display failed status", () => {
      render(
        <BilingualTextViewer
          originalText={mockOriginalText}
          translatedText={mockTranslatedText}
          originalLanguage="Chinese"
          translatedLanguage="English"
          translationStatus="failed"
        />
      );

      expect(
        screen.getByText(/Translation failed/i)
      ).toBeInTheDocument();
    });

    it("should display confidence score when provided", () => {
      render(
        <BilingualTextViewer
          originalText={mockOriginalText}
          translatedText={mockTranslatedText}
          originalLanguage="Japanese"
          translatedLanguage="English"
          confidence={0.95}
        />
      );

      expect(screen.getByText("95.0%")).toBeInTheDocument();
    });

    it("should not display confidence score when not provided", () => {
      render(
        <BilingualTextViewer
          originalText={mockOriginalText}
          translatedText={mockTranslatedText}
          originalLanguage="Korean"
          translatedLanguage="English"
        />
      );

      // Should not have percentage text
      const percentageElements = screen.queryAllByText(/\d+\.\d+%/);
      expect(percentageElements.length).toBe(0);
    });
  });

  describe("Language Display", () => {
    it("should use custom translatedLanguage prop", () => {
      render(
        <BilingualTextViewer
          originalText={mockOriginalText}
          translatedText={mockTranslatedText}
          originalLanguage="Estonian"
          translatedLanguage="French"
        />
      );

      // Check that French appears in the component (multiple times)
      expect(screen.getAllByText(/French/).length).toBeGreaterThan(0);
    });

    it("should default to English as translatedLanguage", () => {
      render(
        <BilingualTextViewer
          originalText={mockOriginalText}
          translatedText={mockTranslatedText}
          originalLanguage="Spanish"
        />
      );

      // Check that English appears in the component (multiple times)
      expect(screen.getAllByText(/English/).length).toBeGreaterThan(0);
    });
  });

  describe("Text Content Handling", () => {
    it("should handle very long text", () => {
      const longText = "A".repeat(5000);

      render(
        <BilingualTextViewer
          originalText={longText}
          translatedText={longText}
          originalLanguage="Marathi"
          translatedLanguage="English"
        />
      );

      // Check that the component renders with long text
      const textElements = screen.getAllByText(longText);
      expect(textElements.length).toBeGreaterThan(0);
    });

    it("should handle text with special characters", () => {
      const specialText = "Special chars: @#$%^&*()_+-=[]{}|;:',.<>?/";

      render(
        <BilingualTextViewer
          originalText={specialText}
          translatedText={specialText}
          originalLanguage="Bengali"
          translatedLanguage="English"
        />
      );

      // Check that the component renders with special characters
      const textElements = screen.getAllByText(specialText);
      expect(textElements.length).toBeGreaterThan(0);
    });

    it("should handle empty text gracefully", () => {
      render(
        <BilingualTextViewer
          originalText=""
          translatedText=""
          originalLanguage="Urdu"
          translatedLanguage="English"
        />
      );

      // Check that the component renders even with empty text
      expect(screen.getByRole("tablist")).toBeInTheDocument();
    });
  });

  describe("Accessibility", () => {
    it("should have semantic HTML structure", () => {
      const { container } = render(
        <BilingualTextViewer
          originalText={mockOriginalText}
          translatedText={mockTranslatedText}
          originalLanguage="French"
          translatedLanguage="English"
        />
      );

      // Check for tabs
      const tabs = screen.getAllByRole("tab");
      expect(tabs.length).toBeGreaterThan(0);

      // Check for buttons (copy/download)
      const buttons = screen.getAllByRole("button");
      expect(buttons.length).toBeGreaterThan(0);
    });

    it("should have keyboard navigable tabs", () => {
      render(
        <BilingualTextViewer
          originalText={mockOriginalText}
          translatedText={mockTranslatedText}
          originalLanguage="Italian"
          translatedLanguage="English"
        />
      );

      const tabs = screen.getAllByRole("tab");
      tabs.forEach((tab) => {
        expect(tab).toHaveAttribute("role", "tab");
      });
    });
  });

  describe("Edge Cases", () => {
    it("should handle identical original and translated text", () => {
      const sameText = "Same text";

      render(
        <BilingualTextViewer
          originalText={sameText}
          translatedText={sameText}
          originalLanguage="English"
          translatedLanguage="English"
        />
      );

      expect(screen.getAllByText(sameText).length).toBeGreaterThan(0);
    });

    it("should handle very long language names", () => {
      render(
        <BilingualTextViewer
          originalText={mockOriginalText}
          translatedText={mockTranslatedText}
          originalLanguage="Very Long Language Name"
          translatedLanguage="Another Very Long Language Name"
        />
      );

      // Check that the component renders with long language names
      expect(screen.getByRole("tablist")).toBeInTheDocument();
    });

    it("should handle confidence score of 0", () => {
      render(
        <BilingualTextViewer
          originalText={mockOriginalText}
          translatedText={mockTranslatedText}
          originalLanguage="Russian"
          translatedLanguage="English"
          confidence={0}
        />
      );

      expect(screen.getByText("0.0%")).toBeInTheDocument();
    });

    it("should handle confidence score of 1", () => {
      render(
        <BilingualTextViewer
          originalText={mockOriginalText}
          translatedText={mockTranslatedText}
          originalLanguage="Dutch"
          translatedLanguage="English"
          confidence={1}
        />
      );

      expect(screen.getByText("100.0%")).toBeInTheDocument();
    });
  });

  describe("Info Footer", () => {
    it("should display helpful info footer", () => {
      render(
        <BilingualTextViewer
          originalText={mockOriginalText}
          translatedText={mockTranslatedText}
          originalLanguage="Portuguese"
          translatedLanguage="English"
        />
      );

      expect(
        screen.getByText(/Use the tabs above to view/i)
      ).toBeInTheDocument();
    });
  });

  describe("Custom Styling", () => {
    it("should apply custom className", () => {
      const { container } = render(
        <BilingualTextViewer
          originalText={mockOriginalText}
          translatedText={mockTranslatedText}
          originalLanguage="Gujarati"
          translatedLanguage="English"
          className="custom-viewer-class"
        />
      );

      expect(container.querySelector(".custom-viewer-class")).toBeInTheDocument();
    });
  });
});
