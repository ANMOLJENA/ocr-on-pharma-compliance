import { describe, it, expect, vi } from "vitest";
import { render, screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { OCRResultsDisplay } from "./OCRResultsDisplay";

// Mock the language components
vi.mock("@/components/language", () => ({
  LanguageDetectionBadge: ({ detectedLanguage, confidence, error }: any) => (
    <div data-testid="language-detection-badge">
      {error ? (
        <div>Error: {error}</div>
      ) : (
        <div>
          {detectedLanguage} ({(confidence * 100).toFixed(1)}%)
        </div>
      )}
    </div>
  ),
  BilingualTextViewer: ({ originalText, translatedText, originalLanguage }: any) => (
    <div data-testid="bilingual-text-viewer">
      <div>Original ({originalLanguage}): {originalText}</div>
      <div>Translated: {translatedText}</div>
    </div>
  ),
}));

describe("OCRResultsDisplay", () => {
  describe("Rendering", () => {
    it("should render the component with title", () => {
      render(
        <OCRResultsDisplay
          originalText="Sample text"
          detectedLanguage="English"
        />
      );
      expect(screen.getByText("OCR Results")).toBeInTheDocument();
    });

    it("should display no data message when no text is provided", () => {
      render(<OCRResultsDisplay />);
      expect(screen.getByText("No OCR Results")).toBeInTheDocument();
      expect(
        screen.getByText(/Upload a document to see OCR results/)
      ).toBeInTheDocument();
    });

    it("should display loading state", () => {
      render(<OCRResultsDisplay isLoading={true} />);
      expect(screen.getByText("Processing Document...")).toBeInTheDocument();
    });

    it("should display error state", () => {
      const errorMessage = "Failed to process document";
      render(<OCRResultsDisplay error={errorMessage} />);
      expect(screen.getByText("OCR Processing Error")).toBeInTheDocument();
      expect(screen.getByText(errorMessage)).toBeInTheDocument();
    });
  });

  describe("Language Detection Display", () => {
    it("should display language detection badge with detected language", () => {
      render(
        <OCRResultsDisplay
          originalText="Sample text"
          detectedLanguage="Hindi"
          detectedLanguageCode="hi"
          confidence={0.95}
        />
      );
      expect(screen.getByTestId("language-detection-badge")).toBeInTheDocument();
      expect(screen.getByText(/Hindi/)).toBeInTheDocument();
    });

    it("should display translation status when translated", () => {
      render(
        <OCRResultsDisplay
          originalText="नमस्ते"
          translatedText="Hello"
          detectedLanguage="Hindi"
          originalLanguage="Hindi"
          isTranslated={true}
          confidence={0.92}
        />
      );
      expect(screen.getByText(/Translation Status/)).toBeInTheDocument();
      expect(screen.getByText(/Document translated from/i)).toBeInTheDocument();
      expect(screen.getByText("Hindi")).toBeInTheDocument();
    });

    it("should not display translation status when not translated", () => {
      render(
        <OCRResultsDisplay
          originalText="Sample text"
          detectedLanguage="English"
          isTranslated={false}
        />
      );
      expect(screen.queryByText(/Translation Status/)).not.toBeInTheDocument();
    });
  });

  describe("Text Display", () => {
    it("should display original text in overview tab", () => {
      render(
        <OCRResultsDisplay
          originalText="Sample extracted text"
          detectedLanguage="English"
        />
      );
      expect(screen.getByText("Sample extracted text")).toBeInTheDocument();
    });

    it("should display bilingual viewer when translated", () => {
      render(
        <OCRResultsDisplay
          originalText="नमस्ते"
          translatedText="Hello"
          detectedLanguage="Hindi"
          originalLanguage="Hindi"
          isTranslated={true}
        />
      );
      expect(screen.getByTestId("bilingual-text-viewer")).toBeInTheDocument();
    });

    it("should display original and translated text in text tab", async () => {
      const user = userEvent.setup();
      render(
        <OCRResultsDisplay
          originalText="Original text"
          translatedText="Translated text"
          detectedLanguage="Spanish"
          originalLanguage="Spanish"
          isTranslated={true}
        />
      );

      // Click on Text tab
      const textTab = screen.getByRole("tab", { name: /Text/ });
      await user.click(textTab);

      expect(screen.getByText("Original text")).toBeInTheDocument();
      expect(screen.getByText("Translated text")).toBeInTheDocument();
    });
  });

  describe("Details Tab", () => {
    it("should display language information in details tab", async () => {
      const user = userEvent.setup();
      render(
        <OCRResultsDisplay
          originalText="Sample text"
          detectedLanguage="French"
          detectedLanguageCode="fr"
          originalLanguage="French"
          confidence={0.88}
        />
      );

      // Click on Details tab
      const detailsTab = screen.getByRole("tab", { name: /Details/ });
      await user.click(detailsTab);

      expect(screen.getByText("Language Information")).toBeInTheDocument();
      expect(screen.getAllByText("French").length).toBeGreaterThan(0);
      expect(screen.getByText("fr")).toBeInTheDocument();
      expect(screen.getByText("88.0%")).toBeInTheDocument();
    });

    it("should display translation information in details tab", async () => {
      const user = userEvent.setup();
      render(
        <OCRResultsDisplay
          originalText="Original"
          translatedText="Translated"
          detectedLanguage="German"
          originalLanguage="German"
          isTranslated={true}
        />
      );

      // Click on Details tab
      const detailsTab = screen.getByRole("tab", { name: /Details/ });
      await user.click(detailsTab);

      expect(screen.getByText("Translation Information")).toBeInTheDocument();
      expect(screen.getByText("Translated")).toBeInTheDocument();
    });

    it("should display text statistics in details tab", async () => {
      const user = userEvent.setup();
      const originalText = "This is a sample text with multiple words";
      render(
        <OCRResultsDisplay
          originalText={originalText}
          detectedLanguage="English"
        />
      );

      // Click on Details tab
      const detailsTab = screen.getByRole("tab", { name: /Details/ });
      await user.click(detailsTab);

      expect(screen.getByText("Text Statistics")).toBeInTheDocument();
      expect(screen.getByText(originalText.length.toString())).toBeInTheDocument();
    });
  });

  describe("Compliance Status", () => {
    it("should display compliance pass status", () => {
      render(
        <OCRResultsDisplay
          originalText="Sample text"
          detectedLanguage="English"
          complianceStatus="pass"
          complianceMessage="Document is compliant"
        />
      );
      expect(screen.getByText("Compliant")).toBeInTheDocument();
      expect(screen.getByText("Document is compliant")).toBeInTheDocument();
    });

    it("should display compliance fail status", () => {
      render(
        <OCRResultsDisplay
          originalText="Sample text"
          detectedLanguage="English"
          complianceStatus="fail"
          complianceMessage="Document is non-compliant"
        />
      );
      expect(screen.getByText("Non-Compliant")).toBeInTheDocument();
      expect(screen.getByText("Document is non-compliant")).toBeInTheDocument();
    });

    it("should display compliance warning status", () => {
      render(
        <OCRResultsDisplay
          originalText="Sample text"
          detectedLanguage="English"
          complianceStatus="warning"
          complianceMessage="Document requires review"
        />
      );
      expect(screen.getByText("Review Required")).toBeInTheDocument();
      expect(screen.getByText("Document requires review")).toBeInTheDocument();
    });
  });

  describe("Tab Navigation", () => {
    it("should switch between tabs", async () => {
      const user = userEvent.setup();
      render(
        <OCRResultsDisplay
          originalText="Sample text"
          detectedLanguage="English"
        />
      );

      // Overview tab should be active by default
      expect(screen.getByText("Sample text")).toBeInTheDocument();

      // Click on Details tab
      const detailsTab = screen.getByRole("tab", { name: /Details/ });
      await user.click(detailsTab);

      expect(screen.getByText("Language Information")).toBeInTheDocument();
    });

    it("should display all three tabs", () => {
      render(
        <OCRResultsDisplay
          originalText="Sample text"
          detectedLanguage="English"
        />
      );

      expect(screen.getByRole("tab", { name: /Overview/ })).toBeInTheDocument();
      expect(screen.getByRole("tab", { name: /Text/ })).toBeInTheDocument();
      expect(screen.getByRole("tab", { name: /Details/ })).toBeInTheDocument();
    });
  });

  describe("Edge Cases", () => {
    it("should handle empty original text gracefully", () => {
      render(
        <OCRResultsDisplay
          originalText=""
          detectedLanguage="English"
        />
      );
      expect(screen.getByText("No OCR Results")).toBeInTheDocument();
    });

    it("should handle missing language information", () => {
      render(
        <OCRResultsDisplay
          originalText="Sample text"
          detectedLanguage={undefined}
        />
      );
      expect(screen.getByText("OCR Results")).toBeInTheDocument();
    });

    it("should handle very long text", () => {
      const longText = "A".repeat(10000);
      render(
        <OCRResultsDisplay
          originalText={longText}
          detectedLanguage="English"
        />
      );
      expect(screen.getByText("OCR Results")).toBeInTheDocument();
    });

    it("should handle multiline text", () => {
      const multilineText = "Line 1\nLine 2\nLine 3";
      render(
        <OCRResultsDisplay
          originalText={multilineText}
          detectedLanguage="English"
        />
      );
      expect(screen.getByText("OCR Results")).toBeInTheDocument();
    });
  });

  describe("Accessibility", () => {
    it("should have proper heading hierarchy", () => {
      render(
        <OCRResultsDisplay
          originalText="Sample text"
          detectedLanguage="English"
        />
      );
      const heading = screen.getByRole("heading", { name: /OCR Results/ });
      expect(heading).toBeInTheDocument();
    });

    it("should have accessible tabs", () => {
      render(
        <OCRResultsDisplay
          originalText="Sample text"
          detectedLanguage="English"
        />
      );
      const tabs = screen.getAllByRole("tab");
      expect(tabs.length).toBe(3);
      tabs.forEach((tab) => {
        expect(tab).toHaveAttribute("role", "tab");
      });
    });
  });
});
