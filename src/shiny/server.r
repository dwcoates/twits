library(shiny)
library(data.table)

tweets <- fread("../../data/processed_toy_sample_tweets.csv")

tweets$color <- ifelse(tweets$retweet_count > 0, "orange", "grey")
tweets$alpha <- ifelse(tweets$user_favourites_count > 0, 0.9, 0.25)

# Define server logic required to draw a histogram
function(input, output) {

  # Expression that generates a histogram. The expression is
  # wrapped in a call to renderPlot to indicate that:
  #
  #  1) It is "reactive" and therefore should be automatically
  #     re-executed when inputs change
  #  2) Its output type is a plot

  output$distPlot <- renderPlot({
    tweets[(tweets$day == input$day) & (tweets$retweet_count > input$retweets)]

    ggplot(r, aes(x = tweets$retweet_count,
                  y = tweets$user_favourites_count,
                  color = price.range)) +
        geom_point() +
        guides(color=tweets$color) +
        ## scale_y_continuous(limits = c(0, 1)) +
        ## scale_x_continuous(limits = c(0, 1)) +
        ggtitle("Low Price Businesses")
  })}
